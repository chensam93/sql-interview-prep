-- Session bootstrap (run once in a fresh SQL tab/session).
-- We attach workspace_build because it is refreshed directly by bootstrap.
attach if not exists 'data/duckdb/workspace_build.duckdb' as workspace_db;

-- If this tab already attached workspace_db to an older file, run this reset block:
-- use memory.main;
-- detach workspace_db;
-- attach 'data/duckdb/workspace_build.duckdb' as workspace_db;

-- Quick sanity checks
-- You can only set one default schema per session (USE). To see every question
-- schema after ATTACH, run the block below, then set USE to one of those names.
--
-- SELECT schema_name
-- FROM information_schema.schemata
-- WHERE catalog_name = 'workspace_db'
--   AND schema_name NOT IN ('information_schema', 'pg_catalog', 'main')
-- ORDER BY schema_name;
--
-- Switch question: edit the single USE line (or skip USE and qualify tables as
-- workspace_db.<schema>.<table>).
USE workspace_db.q003_lower;

SELECT current_database(), current_schema();
SHOW TABLES;

-- Start your answer below
-- SELECT ...

select 
    tickets.*,
    ticket_updates.* 
from tickets
left join ticket_updates
    on ticket_updates.ticket_id = tickets.ticket_id
;

with final as (
    select
        tickets.ticket_id,
        tickets.opened_date,
        tickets.source_channel,
        max(
            case
                when ticket_updates.update_type = 'resolved'
                    and ticket_updates.update_date between tickets.opened_date and tickets.opened_date + interval '7 days'
                then 1
                else 0
            end
        ) as resolved_tickets_7d
    from tickets
    left join ticket_updates
        on ticket_updates.ticket_id = tickets.ticket_id
    group by 1,2,3
)

select
    source_channel,
    count(distinct ticket_id) as opened_tickets,
    sum(resolved_tickets_7d) as resolved_tickets_7d,
    round(100.0 * sum(resolved_tickets_7d) / count(distinct ticket_id), 1) as resolution_rate_pct_7d
from final
group by 1
;