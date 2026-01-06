SELECT
  actor,
  event_date,
  COUNT(*) AS total_events
FROM {{ ref('stg_github_events') }}
GROUP BY actor, event_date
