# Q005 (Core) - Overlapping Subscription Periods Audit

**Level:** Core (mid + senior blend)  
**Concepts tested:** self-join logic, interval overlap checks, deduping pair matches

---

## Scenario

Billing ops wants to catch accounts that have two active subscription records covering the same calendar day.

You have one table:

### `account_subscriptions`
| column | type | description |
|--------|------|-------------|
| `account_id` | varchar | account identifier |
| `subscription_id` | varchar | subscription record identifier |
| `start_date` | date | start of subscription period (inclusive) |
| `end_date` | date | end of subscription period (inclusive) |
| `plan_name` | varchar | plan name |

---

## Question

Return overlapping subscription pairs for the same account.

Output:

- `account_id`
- `subscription_id_a`
- `subscription_id_b`
- `overlap_start_date` (`greatest(start_date_a, start_date_b)`)
- `overlap_end_date` (`least(end_date_a, end_date_b)`)

Rules:

- Only include true overlaps (`overlap_start_date <= overlap_end_date`).
- Do not return duplicate mirrored pairs (`a,b` and `b,a`); return one row per pair.

Order by `account_id`, `subscription_id_a`, `subscription_id_b`.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q005_core;` (see `scratchpad.sql`).
