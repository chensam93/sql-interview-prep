-- Q001 (Core) Reference Solution: Monthly Revenue Trends
-- Statement 1 expected result (exact, 6 rows):
-- order_month, monthly_revenue, three_month_rolling_avg_revenue
-- 2024-01-01, 36337.000, 36337.0
-- 2024-02-01, 24384.000, 30360.5
-- 2024-03-01, 33623.000, 31448.0
-- 2024-04-01, 21923.000, 26643.333333333332
-- 2024-05-01, 31930.000, 29158.666666666668
-- 2024-06-01, 31296.000, 28383.0
--
-- Statement 2 expected result (exact, 6 rows):
-- order_month, product_id, product_revenue
-- 2024-01-01, prod_e, 15496.000
-- 2024-02-01, prod_e, 8021.000
-- 2024-03-01, prod_e, 16538.000
-- 2024-04-01, prod_e, 7361.000
-- 2024-05-01, prod_e, 12393.000
-- 2024-06-01, prod_e, 12520.000

with monthly_revenue as (
    select
        date_trunc('month', orders.order_date)::date as order_month,
        sum(order_items.quantity * order_items.unit_price) as monthly_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        date_trunc('month', orders.order_date)::date
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


with product_monthly_revenue as (
    select
        date_trunc('month', orders.order_date)::date as order_month,
        order_items.product_id,
        sum(order_items.quantity * order_items.unit_price) as product_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        date_trunc('month', orders.order_date)::date,
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
)
select
    ranked_products.order_month,
    ranked_products.product_id,
    ranked_products.product_revenue
from ranked_products
where ranked_products.product_rank = 1
order by ranked_products.order_month;
