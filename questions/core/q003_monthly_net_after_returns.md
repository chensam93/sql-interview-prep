# Q003 (Core) - Monthly gross vs refunds

**Level:** Core (mid + senior blend)  
**Concepts tested:** ctes, joins, aggregation, coalesce, null-safe ratios

---

## Scenario

Finance wants a simple monthly view of how much revenue is given back as refunds.

You have three tables:

### `orders`
| column | type | description |
|--------|------|-------------|
| `order_id` | varchar | unique order identifier |
| `customer_id` | varchar | customer identifier |
| `order_date` | date | order date |
| `channel` | varchar | acquisition channel (`organic`, `paid_search`, `email`) |

### `order_items`
| column | type | description |
|--------|------|-------------|
| `order_id` | varchar | foreign key to orders |
| `product_id` | varchar | product identifier |
| `quantity` | int | quantity purchased |
| `unit_price` | numeric | item unit price |

### `returns`
| column | type | description |
|--------|------|-------------|
| `return_id` | varchar | unique return identifier |
| `order_id` | varchar | foreign key to orders |
| `return_date` | date | when the refund was processed |
| `refund_amount` | numeric | total refund for that return |

---

## Question

Return one row per calendar month that appears in **either** order activity or return activity:

- `report_month` — first day of the month (`date` or `timestamp` truncated to month is fine as long as it sorts correctly)
- `gross_revenue` — sum of `quantity * unit_price` for all line items on orders whose `order_date` falls in that month (use `0` when there were no orders)
- `refund_amount` — sum of `refund_amount` for returns whose `return_date` falls in that month (use `0` when there were no returns)
- `net_revenue` — `gross_revenue - refund_amount`
- `refund_pct_of_gross` — `100 * refund_amount / gross_revenue`, rounded to **two** decimal places; when `gross_revenue` is `0`, this should be `null` (avoid divide-by-zero)

Order by `report_month`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q003_core;` (see `scratchpad.sql`).
