-- Q001 (Lower) Reference Solution: Weekly Ticket Resolution Basics

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
