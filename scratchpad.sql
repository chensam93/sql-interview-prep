-- Session bootstrap (run once in a fresh SQL tab/session).
-- This makes scratchpad self-contained even if DuckDB Explorer is on a different DB.
ATTACH 'data/workspace_verify.duckdb' AS workspace_db;

-- Quick sanity checks
-- Switch questions by changing EXACTLY ONE line below:
-- Q001:
-- USE workspace_db.q001;
-- Q002:
-- USE workspace_db.q002;
USE workspace_db.q002;

SELECT current_database(), current_schema();
SHOW TABLES;

-- Start your answer below
-- SELECT ...
select
    orders.order_id,
    date_trunc('month', orders.order_date) as order_month
from orders
left join order_items
    on orders.order_id = order_items.order_id
;

select count(*), count(distinct order_id) 
from order_items