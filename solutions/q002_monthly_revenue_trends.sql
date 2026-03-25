-- Q002 Reference Solution: Monthly Revenue Trends
-- -----------------------------------------------------------------------------
-- Query 1: monthly revenue + three-month rolling average
-- -----------------------------------------------------------------------------

with monthly_revenue as (
    select
        date_trunc('month', orders.order_date) as order_month,
        sum(order_items.quantity * order_items.unit_price) as monthly_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        date_trunc('month', orders.order_date)
),
monthly_revenue_with_rolling_average as (
    select
        monthly_revenue.order_month,
        monthly_revenue.monthly_revenue,
        avg(monthly_revenue.monthly_revenue) over (
            order by monthly_revenue.order_month
            rows between 2 preceding and current row
        ) as three_month_rolling_avg_revenue
    from monthly_revenue
)
select
    monthly_revenue_with_rolling_average.order_month,
    monthly_revenue_with_rolling_average.monthly_revenue,
    monthly_revenue_with_rolling_average.three_month_rolling_avg_revenue
from monthly_revenue_with_rolling_average
order by monthly_revenue_with_rolling_average.order_month;


-- -----------------------------------------------------------------------------
-- Query 2: top revenue product per month (tie-break on product_id asc)
-- -----------------------------------------------------------------------------

with product_monthly_revenue as (
    select
        date_trunc('month', orders.order_date) as order_month,
        order_items.product_id,
        sum(order_items.quantity * order_items.unit_price) as product_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        date_trunc('month', orders.order_date),
        order_items.product_id
),
ranked_products as (
    select
        product_monthly_revenue.order_month,
        product_monthly_revenue.product_id,
        product_monthly_revenue.product_revenue,
        row_number() over (
            partition by product_monthly_revenue.order_month
            order by
                product_monthly_revenue.product_revenue desc,
                product_monthly_revenue.product_id asc
        ) as product_rank
    from product_monthly_revenue
),
top_product_by_month as (
    select
        ranked_products.order_month,
        ranked_products.product_id,
        ranked_products.product_revenue
    from ranked_products
    where ranked_products.product_rank = 1
)
select
    top_product_by_month.order_month,
    top_product_by_month.product_id,
    top_product_by_month.product_revenue
from top_product_by_month
order by top_product_by_month.order_month;
