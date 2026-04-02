-- Q002 (Core) Reference Solution: Channel Revenue Mix (New vs Returning)

with order_level_revenue as (
    select
        orders.order_id,
        orders.customer_id,
        orders.channel,
        date_trunc('month', orders.order_date)::date as order_month,
        sum(order_items.quantity * order_items.unit_price) as order_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        orders.order_id,
        orders.customer_id,
        orders.channel,
        date_trunc('month', orders.order_date)::date
),
customer_first_order_month as (
    select
        order_level_revenue.customer_id,
        min(order_level_revenue.order_month) as first_order_month
    from order_level_revenue
    group by
        order_level_revenue.customer_id
),
monthly_channel_revenue_mix as (
    select
        order_level_revenue.order_month,
        order_level_revenue.channel,
        sum(order_level_revenue.order_revenue) as gross_revenue,
        sum(
            case
                when order_level_revenue.order_month = customer_first_order_month.first_order_month
                    then order_level_revenue.order_revenue
                else 0
            end
        ) as new_customer_revenue,
        sum(
            case
                when order_level_revenue.order_month > customer_first_order_month.first_order_month
                    then order_level_revenue.order_revenue
                else 0
            end
        ) as returning_customer_revenue
    from order_level_revenue
    inner join customer_first_order_month
        on customer_first_order_month.customer_id = order_level_revenue.customer_id
    group by
        order_level_revenue.order_month,
        order_level_revenue.channel
)
select
    monthly_channel_revenue_mix.order_month,
    monthly_channel_revenue_mix.channel,
    monthly_channel_revenue_mix.gross_revenue,
    monthly_channel_revenue_mix.new_customer_revenue,
    monthly_channel_revenue_mix.returning_customer_revenue,
    round(
        100.0 * monthly_channel_revenue_mix.returning_customer_revenue
        / nullif(monthly_channel_revenue_mix.gross_revenue, 0),
        1
    ) as returning_revenue_share_pct
from monthly_channel_revenue_mix
order by
    monthly_channel_revenue_mix.order_month,
    monthly_channel_revenue_mix.channel;


with order_level_revenue as (
    select
        orders.order_id,
        orders.channel,
        date_trunc('month', orders.order_date)::date as order_month,
        sum(order_items.quantity * order_items.unit_price) as order_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        orders.order_id,
        orders.channel,
        date_trunc('month', orders.order_date)::date
),
monthly_channel_revenue as (
    select
        order_level_revenue.order_month,
        order_level_revenue.channel,
        sum(order_level_revenue.order_revenue) as gross_revenue
    from order_level_revenue
    group by
        order_level_revenue.order_month,
        order_level_revenue.channel
),
monthly_channel_with_delta as (
    select
        monthly_channel_revenue.order_month,
        monthly_channel_revenue.channel,
        monthly_channel_revenue.gross_revenue,
        monthly_channel_revenue.gross_revenue
            - coalesce(
                lag(monthly_channel_revenue.gross_revenue) over (
                    partition by monthly_channel_revenue.channel
                    order by monthly_channel_revenue.order_month
                ),
                0
            ) as mom_revenue_delta
    from monthly_channel_revenue
),
ranked_channels as (
    select
        monthly_channel_with_delta.order_month,
        monthly_channel_with_delta.channel,
        monthly_channel_with_delta.gross_revenue,
        monthly_channel_with_delta.mom_revenue_delta,
        row_number() over (
            partition by monthly_channel_with_delta.order_month
            order by
                monthly_channel_with_delta.mom_revenue_delta desc,
                monthly_channel_with_delta.channel asc
        ) as channel_rank
    from monthly_channel_with_delta
)
select
    ranked_channels.order_month,
    ranked_channels.channel,
    ranked_channels.gross_revenue,
    ranked_channels.mom_revenue_delta
from ranked_channels
where ranked_channels.channel_rank = 1
order by ranked_channels.order_month;
