# Q001 (Lower) - Weekly Ticket Resolution Basics

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** left join filtering, count distinct, date bucketing, case statements, basic percentages

---

## Scenario

You are helping support operations review weekly ticket resolution performance.

You have two tables:

### `tickets`
| column | type | description |
|--------|------|-------------|
| `ticket_id` | varchar | unique ticket identifier |
| `opened_date` | date | when the ticket was opened |
| `priority` | varchar | `low`, `medium`, `high` |
| `source_channel` | varchar | `email`, `chat`, `phone` |

### `ticket_updates`
| column | type | description |
|--------|------|-------------|
| `ticket_id` | varchar | foreign key to tickets |
| `update_date` | date | date of update |
| `update_type` | varchar | `comment`, `resolved`, `reopened` |

---

## Question

Return one row per `opened_week` and `priority` with:

- `opened_week` (week of `opened_date`)
- `priority`
- `opened_tickets` (distinct tickets opened in that week/priority)
- `resolved_tickets_3d` (distinct tickets with at least one `resolved` update from opened date through opened date + 3 days)
- `unresolved_tickets_3d` (`opened_tickets - resolved_tickets_3d`)
- `resolution_rate_pct_3d` (`100 * resolved_tickets_3d / opened_tickets`, rounded to one decimal)
- `resolution_band`:
  - `strong` when rate >= 70
  - `ok` when rate >= 40 and < 70
  - `weak` otherwise

Notes:
- Keep tickets even when they have no updates.
- A ticket should only be counted once in `resolved_tickets_3d`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q001_lower;` (see `scratchpad.sql`).
