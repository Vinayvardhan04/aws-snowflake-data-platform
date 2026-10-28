with ranked as (
    select
        event_id,
        event_type,
        repo_name,
        actor,
        created_at,
        event_date,
        row_number() over (partition by event_id order by created_at desc) as event_rank
    from DE_PLATFORM.RAW.GITHUB_EVENTS
    where event_id is not null
      and repo_name is not null
      and actor is not null
)
select event_id, event_type, repo_name, actor, created_at, event_date
from ranked
where event_rank = 1
