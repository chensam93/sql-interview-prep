# Q006 (Lower) - Refund Without Return

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** joins, existence checks, filtering

---

## Scenario

You are checking order event consistency.

You have two tables:

### `orders`
| column | type | description |
|--------|------|-------------|
| `order_id` | varchar | order identifier |
| `customer_id` | varchar | customer identifier |
| `order_date` | date | date order was placed |

### `order_events`
| column | type | description |
|--------|------|-------------|
| `order_id` | varchar | order identifier |
| `event_date` | date | event date |
| `event_type` | varchar | event type (`placed`, `shipped`, `returned`, `refunded`) |

---

## Question

Return orders that have at least one `refunded` event but **no** `returned` event.

Output columns:

- `order_id`
- `customer_id`
- `order_date`

Order by `order_id`.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q006_lower;` (see `scratchpad.sql`).
