# Q002 - Monthly Revenue Trends

**Level:** Senior Analytics Engineer  
**Concepts tested:** aggregation, window functions, ranking

---

## Scenario

You work at an e-commerce company. Finance wants a quick monthly revenue trend view and product performance snapshot.

You have two tables:

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

---

## Questions

### Query 1
Return one row per month with:
- `order_month`
- `monthly_revenue` (sum of `quantity * unit_price`)
- `three_month_rolling_avg_revenue` (current month + prior 2 months)

Helpful notes:
- A 3-month rolling average at month `M` means averaging revenue for `M`, `M-1`, and `M-2`.
- For early months with fewer than 3 months of history, use whatever rows exist so far.
  - Example: if only Jan and Feb exist, Feb's rolling average uses Jan+Feb.

### Query 2
For each month, return the **top revenue product** with:
- `order_month`
- `product_id`
- `product_revenue`

If there is a tie, keep the product with the alphabetically smallest `product_id`.

Helpful note:
- This is usually done with a window rank (for example `row_number`) partitioned by month.

---

## Data

Connect to: `data/workspace.duckdb` and run `SET schema = 'q002';`

If you open `data/q002.duckdb` directly instead, tables live in schema `main` — do not use `SET schema = 'q002'`. After adding or changing generators, run `python data/bootstrap.py` so `workspace.duckdb` includes the `q002` schema.
