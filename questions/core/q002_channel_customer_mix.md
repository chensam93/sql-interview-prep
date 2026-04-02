# Q002 (Core) - Channel Revenue Mix (New vs Returning)

**Level:** Core (mid + senior blend)  
**Concepts tested:** ctes, window functions, conditional aggregation, ranking

---

## Scenario

Marketing wants a monthly view of revenue quality by acquisition channel.

You have two tables:

### `orders`
| column | type | description |
|--------|------|-------------|
| `order_id` | varchar | unique order identifier |
| `customer_id` | varchar | customer identifier |
| `order_date` | date | order date |
| `channel` | varchar | acquisition channel (`organic`, `paid_search`, `email`, `affiliate`) |

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
Return one row per `order_month` and `channel` with:
- `order_month`
- `channel`
- `gross_revenue`
- `new_customer_revenue` (revenue from a customer’s first-ever order month)
- `returning_customer_revenue` (all other revenue)
- `returning_revenue_share_pct` (`returning_customer_revenue / gross_revenue * 100`)

Helpful notes:
- Treat "new customer" at a month grain: if a customer’s first order is in month `M`, all their revenue in `M` is "new".
- Revenue is `sum(quantity * unit_price)`.

### Query 2
For each month, return the channel with the largest month-over-month increase in `gross_revenue`.

Output:
- `order_month`
- `channel`
- `gross_revenue`
- `mom_revenue_delta`

Rules:
- `mom_revenue_delta = current_month_revenue - prior_month_revenue` by channel.
- If a prior month is missing for that channel, treat prior revenue as `0`.
- If there is a tie, keep the alphabetically smallest `channel`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q002_core;` (see `scratchpad.sql`).
