select
    repo_name,
    event_date,
    count(*) as total_events,
    count(distinct actor) as distinct_actors
from {{ ref('stg_github_events') }}
group by repo_name, event_date
