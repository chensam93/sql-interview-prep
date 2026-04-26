-- Q003 (Lower) Reference Solution: Priority Mix by Channel
-- Expected result (exact, 3 rows):
-- source_channel, total_tickets, high_priority_tickets, high_priority_pct, priority_risk_band
-- chat, 194, 39, 20.1, medium_risk
-- email, 342, 51, 14.9, low_risk
-- phone, 124, 40, 32.3, high_risk

with channel_priority_counts as (
    select
        tickets.source_channel,
        count(distinct tickets.ticket_id) as total_tickets,
        count(
            distinct case
                when tickets.priority = 'high' then tickets.ticket_id
                else null
            end
        ) as high_priority_tickets
    from tickets
    group by
        tickets.source_channel
)
select
    channel_priority_counts.source_channel,
    channel_priority_counts.total_tickets,
    channel_priority_counts.high_priority_tickets,
    round(
        100.0 * channel_priority_counts.high_priority_tickets
            / channel_priority_counts.total_tickets,
        1
    ) as high_priority_pct,
    case
        when 100.0 * channel_priority_counts.high_priority_tickets
            / channel_priority_counts.total_tickets >= 30
        then 'high_risk'
        when 100.0 * channel_priority_counts.high_priority_tickets
            / channel_priority_counts.total_tickets >= 15
        then 'medium_risk'
        else 'low_risk'
    end as priority_risk_band
from channel_priority_counts
order by channel_priority_counts.source_channel;
