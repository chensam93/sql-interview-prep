-- Q002 (Lower) Reference Solution: 7-Day Resolution Rate by Channel
-- Expected result (exact, 3 rows):
-- source_channel, opened_tickets, resolved_tickets_7d, resolution_rate_pct_7d
-- chat, 224, 116, 51.8
-- email, 371, 150, 40.4
-- phone, 125, 55, 44.0

with ticket_resolution_flags as (
    select
        tickets.ticket_id,
        tickets.source_channel,
        max(
            case
                when ticket_updates.update_type = 'resolved'
                    and ticket_updates.update_date >= tickets.opened_date
                    and ticket_updates.update_date <= tickets.opened_date + interval '7 day'
                then 1
                else 0
            end
        ) as has_resolution_7d
    from tickets
    left join ticket_updates
        on ticket_updates.ticket_id = tickets.ticket_id
    group by
        tickets.ticket_id,
        tickets.source_channel
),
channel_rollup as (
    select
        ticket_resolution_flags.source_channel,
        count(*) as opened_tickets,
        sum(ticket_resolution_flags.has_resolution_7d) as resolved_tickets_7d
    from ticket_resolution_flags
    group by
        ticket_resolution_flags.source_channel
)
select
    channel_rollup.source_channel,
    channel_rollup.opened_tickets,
    channel_rollup.resolved_tickets_7d,
    round(
        100.0 * channel_rollup.resolved_tickets_7d / channel_rollup.opened_tickets,
        1
    ) as resolution_rate_pct_7d
from channel_rollup
order by channel_rollup.source_channel;
