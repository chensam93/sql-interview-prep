-- Q005 (Lower) Reference Solution: Duplicate Snapshot Keys
-- Expected result (exact, 4 rows):
-- store_id, product_id, snapshot_date, duplicate_count
-- store_002, prod_b, 2024-08-10, 3
-- store_003, prod_d, 2024-08-12, 3
-- store_001, prod_c, 2024-08-04, 2
-- store_003, prod_a, 2024-08-08, 2

with duplicate_snapshot_keys as (
    select
        inventory_snapshots.store_id,
        inventory_snapshots.product_id,
        inventory_snapshots.snapshot_date,
        count(*) as duplicate_count
    from inventory_snapshots
    group by
        inventory_snapshots.store_id,
        inventory_snapshots.product_id,
        inventory_snapshots.snapshot_date
    having count(*) > 1
)
select
    duplicate_snapshot_keys.store_id,
    duplicate_snapshot_keys.product_id,
    duplicate_snapshot_keys.snapshot_date,
    duplicate_snapshot_keys.duplicate_count
from duplicate_snapshot_keys
order by
    duplicate_snapshot_keys.duplicate_count desc,
    duplicate_snapshot_keys.store_id,
    duplicate_snapshot_keys.product_id,
    duplicate_snapshot_keys.snapshot_date;
