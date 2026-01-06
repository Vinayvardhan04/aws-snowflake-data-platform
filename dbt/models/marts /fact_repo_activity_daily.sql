SELECT
  repo_name,
  event_date,
  COUNT(*) AS total_events
FROM {{ ref('stg_github_events') }}
GROUP BY repo_name, event_date
