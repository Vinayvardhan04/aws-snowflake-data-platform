SELECT
  event_id,
  event_type,
  repo_name,
  actor,
  created_at,
  event_date
FROM DE_PLATFORM.RAW.GITHUB_EVENTS
WHERE event_id IS NOT NULL
