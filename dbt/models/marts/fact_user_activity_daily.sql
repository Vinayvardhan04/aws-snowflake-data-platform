select
    actor,
    event_date,
    count(*) as total_events,
    count(distinct repo_name) as distinct_repositories
from {{ ref('stg_github_events') }}
group by actor, event_date
