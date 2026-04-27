-- Q006 (Lower) Reference Solution: Refund Without Return
-- Expected output (sample, first 5 rows):
-- order_id, customer_id, order_date
-- order_00000, cust_001, 2024-09-01
-- order_00012, cust_013, 2024-09-13
-- order_00024, cust_025, 2024-09-04
-- order_00036, cust_037, 2024-09-16
-- order_00048, cust_004, 2024-09-07

with refunded_orders as (
    select distinct
        order_events.order_id
    from order_events
    where order_events.event_type = 'refunded'
),
returned_orders as (
    select distinct
        order_events.order_id
    from order_events
    where order_events.event_type = 'returned'
),
refund_without_return_orders as (
    select
        refunded_orders.order_id
    from refunded_orders
    left join returned_orders
        on refunded_orders.order_id = returned_orders.order_id
    where returned_orders.order_id is null
)
select
    orders.order_id,
    orders.customer_id,
    orders.order_date
from orders
inner join refund_without_return_orders
    on orders.order_id = refund_without_return_orders.order_id
order by
    orders.order_id;
