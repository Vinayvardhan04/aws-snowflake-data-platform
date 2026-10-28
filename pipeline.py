"""Small, reproducible GitHub Events ETL with a local SQLite warehouse."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("event_id", "event_type", "repo_name", "actor", "created_at", "event_date")


def fetch_events(source: str) -> list[dict]:
    if source == "github":
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "vinay-github-events-demo"}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
        request = urllib.request.Request("https://api.github.com/events?per_page=100", headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    else:
        with Path(source).open(encoding="utf-8") as source_file:
            data = json.load(source_file)
    if not isinstance(data, list):
        raise ValueError("The input must be a JSON array of GitHub events")
    return data


def normalize(event: dict) -> dict:
    if any(value is None for value in (
        event["id"], event["type"], event["repo"]["name"],
        event["actor"]["login"], event["created_at"]
    )):
        raise ValueError("Missing required field")
    event_id = str(event["id"]).strip()
    event_type = str(event["type"]).strip()
    repo_name = str(event["repo"]["name"]).strip()
    actor = str(event["actor"]["login"]).strip()
    timestamp = datetime.fromisoformat(str(event["created_at"]).replace("Z", "+00:00"))
    if not all((event_id, event_type, repo_name, actor)) or timestamp.tzinfo is None:
        raise ValueError("Missing required field or timezone")
    timestamp = timestamp.astimezone(timezone.utc)
    return dict(zip(FIELDS, (event_id, event_type, repo_name, actor,
                             timestamp.isoformat(timespec="seconds"), timestamp.date().isoformat())))


def create_database(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        actor TEXT NOT NULL,
        created_at TEXT NOT NULL,
        event_date TEXT NOT NULL
    )""")
    connection.execute("CREATE INDEX IF NOT EXISTS ix_events_repo_date ON events(repo_name, event_date)")


def run(source: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bronze = output_dir / "bronze"
    silver = output_dir / "silver"
    bronze.mkdir(exist_ok=True)
    silver.mkdir(exist_ok=True)
    raw = fetch_events(source)
    (bronze / "events.json").write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    valid: list[dict] = []
    invalid = 0
    seen: set[str] = set()
    duplicates = 0
    for item in raw:
        try:
            row = normalize(item)
        except (KeyError, TypeError, ValueError, AttributeError):
            invalid += 1
            continue
        if row["event_id"] in seen:
            duplicates += 1
            continue
        seen.add(row["event_id"])
        valid.append(row)

    with (silver / "events.jsonl").open("w", encoding="utf-8") as file:
        for row in valid:
            file.write(json.dumps(row) + "\n")

    with sqlite3.connect(output_dir / "events.sqlite3") as connection:
        create_database(connection)
        before = connection.total_changes
        connection.executemany(
            "INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?, ?, ?)",
            [tuple(row[key] for key in FIELDS) for row in valid],
        )
        loaded = connection.total_changes - before
        metrics = connection.execute("""SELECT repo_name, event_date, COUNT(*)
            FROM events GROUP BY repo_name, event_date ORDER BY event_date, repo_name""").fetchall()

    print(f"received={len(raw)} valid={len(valid)} invalid={invalid} duplicate_in_batch={duplicates} newly_loaded={loaded}")
    for repo_name, event_date, count in metrics:
        print(f"{event_date} {repo_name}: {count} event(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="sample_data/events.json", help="JSON file or 'github'")
    parser.add_argument("--output-dir", type=Path, default=Path(".local"))
    arguments = parser.parse_args()
    run(arguments.source, arguments.output_dir)
