-- Q003 (Core) Reference Solution: Monthly gross vs refunds
-- Expected result (exact, 6 rows):
-- report_month, gross_revenue, refund_amount, net_revenue, refund_pct_of_gross
-- 2024-01-01, 19781.500, 432.500, 19349.000, 2.19
-- 2024-02-01, 19295.500, 1201.760, 18093.740, 6.23
-- 2024-03-01, 18591.500, 1852.880, 16738.620, 9.97
-- 2024-04-01, 19063.500, 2084.380, 16979.120, 10.93
-- 2024-05-01, 19598.500, 1674.760, 17923.740, 8.55
-- 2024-06-01, 18651.000, 2754.490, 15896.510, 14.77

with monthly_gross_revenue as (
    select
        date_trunc('month', orders.order_date)::date as report_month,
        sum(order_items.quantity * order_items.unit_price) as gross_revenue
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        date_trunc('month', orders.order_date)::date
),
monthly_refund_amounts as (
    select
        date_trunc('month', returns.return_date)::date as report_month,
        sum(returns.refund_amount) as refund_amount
    from returns
    group by
        date_trunc('month', returns.return_date)::date
),
all_report_months as (
    select
        monthly_gross_revenue.report_month
    from monthly_gross_revenue
    union
    select
        monthly_refund_amounts.report_month
    from monthly_refund_amounts
)
select
    all_report_months.report_month,
    coalesce(monthly_gross_revenue.gross_revenue, 0) as gross_revenue,
    coalesce(monthly_refund_amounts.refund_amount, 0) as refund_amount,
    coalesce(monthly_gross_revenue.gross_revenue, 0)
        - coalesce(monthly_refund_amounts.refund_amount, 0) as net_revenue,
    round(
        100.0 * coalesce(monthly_refund_amounts.refund_amount, 0)
            / nullif(coalesce(monthly_gross_revenue.gross_revenue, 0), 0),
        2
    ) as refund_pct_of_gross
from all_report_months
left join monthly_gross_revenue
    on monthly_gross_revenue.report_month = all_report_months.report_month
left join monthly_refund_amounts
    on monthly_refund_amounts.report_month = all_report_months.report_month
order by
    all_report_months.report_month;
