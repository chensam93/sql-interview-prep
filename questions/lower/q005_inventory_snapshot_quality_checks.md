# Q005 (Lower) - Duplicate Snapshot Keys

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** grouped duplicate detection, `having`, basic ordering

---

## Scenario

You are reviewing a retail inventory snapshot feed and need to find duplicate daily keys.

You have one table:

### `inventory_snapshots`
| column | type | description |
|--------|------|-------------|
| `store_id` | varchar | store identifier |
| `product_id` | varchar | product identifier |
| `snapshot_date` | date | date of inventory snapshot |
| `on_hand_qty` | integer | on-hand quantity recorded for that day |

---

## Question

Return one row per duplicate key where the same (`store_id`, `product_id`, `snapshot_date`) appears more than once.

Output columns:

- `store_id`
- `product_id`
- `snapshot_date`
- `duplicate_count`

Order by `duplicate_count` descending, then `store_id`, `product_id`, `snapshot_date`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q005_lower;` (see `scratchpad.sql`).
