# Q001 — Cohort Retention Analysis

**Level:** Senior Analytics Engineer  
**Concepts tested:** cohort bucketing, date math, window functions vs self-join, sparse data handling, ratio calculations

---

## Scenario

You work at a B2C SaaS company. The growth team wants to understand how well the product retains users after signup.

You have two tables available:

### `users`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | unique user identifier |
| `signup_date` | date | date the user created their account |
| `channel` | varchar | acquisition channel (`organic`, `paid_social`, `referral`) |
| `plan_type` | varchar | `free` or `premium` |

### `activity`
| column | type | description |
|--------|------|-------------|
| `user_id` | varchar | foreign key to users |
| `activity_date` | date | date of any product activity |
| `activity_type` | varchar | `login`, `feature_use`, `purchase` |

---

## Questions

### Part A (core)
Calculate **weekly signup cohort retention** at **Day 1**, **Day 7**, and **Day 30**.

Output one row per cohort week with:
- `cohort_week` — the Monday-start week of signup
- `cohort_size` — number of users who signed up that week
- `retained_d1` — users active on day 1 (activity_date = signup_date + 1)
- `retained_d7` — users active on day 7 (activity_date = signup_date + 7)
- `retained_d30` — users active on day 30 (activity_date = signup_date + 30)
- `retention_rate_d1`, `retention_rate_d7`, `retention_rate_d30` — as percentages (0–100)

### Part B (follow-up)
The growth team also wants to compare retention between `free` and `premium` users.  
Extend Part A to break out by `plan_type`.

### Part C (discussion)
- How would you handle cohorts that are too recent to have hit their D30 window yet?
- A user could have multiple activity records on the same day. Does that affect your query? Should it?
- If this were a dbt model, what grain would you choose? Incremental or full refresh?

---

## Data

Connect to: `data/q001.duckdb`

Tables: `users`, `activity`

Sample size: ~1,500 users, ~18,000 activity events over ~90 days

---

## Hints (expand if stuck)

<details>
<summary>Hint 1</summary>
Try joining users to activity once per retention milestone rather than doing it all in one pass.
</details>

<details>
<summary>Hint 2</summary>
A user retained on D7 means their activity_date equals exactly signup_date + 7, OR any day within that window? Clarify the definition before writing SQL.
</details>

<details>
<summary>Hint 3</summary>
Use `date_trunc('week', signup_date)` for cohort bucketing. Consider whether you want Monday or Sunday week starts.
</details>
