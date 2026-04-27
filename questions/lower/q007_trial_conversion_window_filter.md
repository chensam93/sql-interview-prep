# Q007 (Lower) - Trial Conversion Window Filter

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** joins, date interval filtering, include/exclude conditions

---

## Scenario

You are reviewing trial users who converted quickly.

You have two tables:

### `trial_signups`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | user identifier |
| `signup_date` | date | trial signup date |

### `subscriptions`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | user identifier |
| `subscription_start_date` | date | paid subscription start date |
| `plan_name` | varchar | subscription plan (`basic`, `pro`) |

---

## Question

Return users who started a paid subscription within **0 to 7 days** (inclusive) after `signup_date`.

Output columns:

- `user_id`
- `signup_date`
- `subscription_start_date`
- `days_to_convert` (`subscription_start_date - signup_date`)

Exclude users with no subscription.

Order by `user_id`.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q007_lower;` (see `scratchpad.sql`).
