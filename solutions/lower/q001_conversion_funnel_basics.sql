-- Q001 (Lower) Reference Solution: Weekly Ticket Resolution Basics
-- Expected result shape: 42 rows.
-- Expected output preview (ordered by opened_week, priority):
-- opened_week, priority, opened_tickets, resolved_tickets_3d, unresolved_tickets_3d, resolution_rate_pct_3d, resolution_band
-- 2024-01-29, high, 11, 4, 7, 36.4, weak
-- 2024-01-29, low, 19, 4, 15, 21.1, weak
-- 2024-01-29, medium, 7, 3, 4, 42.9, ok
-- 2024-02-05, high, 7, 4, 3, 57.1, ok
-- 2024-02-05, low, 25, 9, 16, 36.0, weak

with ticket_resolution_flags as (
    select
        tickets.ticket_id,
        date_trunc('week', tickets.opened_date)::date as opened_week,
        tickets.priority,
        max(
            case
                when ticket_updates.update_type = 'resolved'
                    and ticket_updates.update_date >= tickets.opened_date
                    and ticket_updates.update_date <= tickets.opened_date + interval '3 day'
                then 1
                else 0
            end
        ) as has_resolution_3d
    from tickets
    left join ticket_updates
        on ticket_updates.ticket_id = tickets.ticket_id
    group by
        tickets.ticket_id,
        date_trunc('week', tickets.opened_date)::date,
        tickets.priority
),
weekly_priority_rollup as (
    select
        ticket_resolution_flags.opened_week,
        ticket_resolution_flags.priority,
        count(*) as opened_tickets,
        sum(ticket_resolution_flags.has_resolution_3d) as resolved_tickets_3d
    from ticket_resolution_flags
    group by
        ticket_resolution_flags.opened_week,
        ticket_resolution_flags.priority
)
select
    weekly_priority_rollup.opened_week,
    weekly_priority_rollup.priority,
    weekly_priority_rollup.opened_tickets,
    weekly_priority_rollup.resolved_tickets_3d,
    weekly_priority_rollup.opened_tickets - weekly_priority_rollup.resolved_tickets_3d as unresolved_tickets_3d,
    round(
        100.0 * weekly_priority_rollup.resolved_tickets_3d
            / weekly_priority_rollup.opened_tickets,
        1
    ) as resolution_rate_pct_3d,
    case
        when 100.0 * weekly_priority_rollup.resolved_tickets_3d
            / weekly_priority_rollup.opened_tickets >= 70
        then 'strong'
        when 100.0 * weekly_priority_rollup.resolved_tickets_3d
            / weekly_priority_rollup.opened_tickets >= 40
        then 'ok'
        else 'weak'
    end as resolution_band
from weekly_priority_rollup
order by
    weekly_priority_rollup.opened_week,
    weekly_priority_rollup.priority;
