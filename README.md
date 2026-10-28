# GitHub Events Data Platform

A portfolio data engineering project built around GitHub's public Events API. The **local path runs with Python's standard library and SQLite**: it ingests raw JSON, validates and deduplicates events, loads a warehouse table, and prints daily activity metrics. The repository also includes dbt models for Snowflake and Terraform for AWS storage. Cloud resources are templates and have **not** been deployed as part of this repository.

## What it demonstrates

- Idempotent ingestion: the GitHub event ID is the warehouse primary key, so reruns do not double count events.
- Data quality gates: required fields, parseable UTC timestamps, and an explicit invalid-record count.
- Bronze and silver artifacts: raw responses and normalized records are saved separately.
- SQL analytics: daily repository and actor activity with a reproducible local query.
- Cloud design: Snowflake staging/marts and least-privilege S3 bucket configuration.

## Run locally

```bash
python3 pipeline.py --source sample_data/events.json --output-dir .local
python3 pipeline.py --source sample_data/events.json --output-dir .local
```

The second run reports zero newly loaded rows. `.local/` is ignored by Git. To fetch current public events instead:

```bash
python3 pipeline.py --source github --output-dir .local
```

GitHub's unauthenticated API is rate limited. Set `GITHUB_TOKEN` in your shell for a higher rate limit; never commit it. The example does not require a token.

## Architecture

```text
GitHub Events API or sample JSON
           |
           v
    bronze/events.json
           |
      validation + normalization
           |
           v
    silver/events.jsonl ----> SQLite events table ----> daily SQL metrics
                                     |
                          optional Snowflake/dbt path
```

`pipeline.py` is the runnable local implementation. `snowflake/setup.sql` and `dbt/` show how the same normalized fields map to an analytics warehouse. `terraform/` provisions private S3 buckets for a cloud deployment; it does not wire up Lambda, Glue, Airflow, or a Snowflake storage integration. Those are documented next steps, not completed features.

## Data model

| Field | Description |
|---|---|
| `event_id` | Unique GitHub event ID; deduplication key |
| `event_type` | GitHub event category |
| `repo_name` | `owner/repository` |
| `actor` | Login of the event actor |
| `created_at` | Event timestamp in UTC |
| `event_date` | UTC calendar date derived from `created_at` |

## Repository map

- [`pipeline.py`](pipeline.py): runnable ingestion, quality checks, SQLite load, and report.
- [`sample_data/events.json`](sample_data/events.json): small deterministic input, including a duplicate and an invalid record.
- [`dbt/models`](dbt/models): Snowflake staging and daily marts.
- [`snowflake/setup.sql`](snowflake/setup.sql): warehouse and raw table DDL.
- [`terraform`](terraform): S3 storage with encryption and public access blocked.
- [`docs/architecture.md`](docs/architecture.md): design decisions, limitations, and production extension plan.

## Reproduce the results

The sample has four records: two valid unique events, one duplicate ID, and one invalid timestamp. A fresh run loads two rows, reports one duplicate and one invalid record, and produces one event each for `acme/api` and `acme/web` on 2026-10-20. This is an illustrative dataset, not a claimed production deployment.

## License

MIT; see [LICENSE](LICENSE).
