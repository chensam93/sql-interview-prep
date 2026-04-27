# Q008 (Lower) - Failed Logins Before First Success

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** first-occurrence logic, conditional counting, joins

---

## Scenario

You are reviewing authentication friction for users.

You have one table:

### `auth_events`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | user identifier |
| `event_time` | timestamp | event timestamp |
| `event_type` | varchar | login event (`failed_login`, `successful_login`) |

---

## Question

Return users who had **at least 3 failed logins before their first successful login**.

Output columns:

- `user_id`
- `first_success_time`
- `failed_attempts_before_success`

Exclude users who never had a `successful_login`.

Order by `user_id`.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q008_lower;` (see `scratchpad.sql`).
