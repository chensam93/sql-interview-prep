# Q001 (Lower) - Conversion Funnel Basics

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** staged aggregation, distinct users, conversion rates

---

## Scenario

You are helping growth review signup funnel performance by signup week.

You have two tables:

### `signups`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | unique user id |
| `signup_date` | date | signup date |
| `acquisition_channel` | varchar | `organic`, `paid_search`, `referral`, `social` |

### `events`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | foreign key to signups |
| `event_date` | date | date of event |
| `event_name` | varchar | `signup_complete`, `profile_complete`, `first_purchase` |

---

## Questions

### Query 1
Return one row per signup week with:
- `signup_week`
- `signed_up_users`
- `profile_completed_users` (within 14 days of signup)
- `purchased_users` (within 30 days of signup)
- `profile_completion_rate_pct`
- `purchase_rate_pct`

### Query 2
For each signup week, show which `acquisition_channel` had the most purchasers (same 30-day rule).

If there is a tie, keep the alphabetically smallest `acquisition_channel`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q001_lower;` (see `scratchpad.sql`).
