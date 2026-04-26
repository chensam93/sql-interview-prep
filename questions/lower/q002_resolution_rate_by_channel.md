# Q002 (Lower) - 7-Day Resolution Rate by Channel

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** left join filtering, case statements, grouped aggregation, basic percentages

---

## Scenario

You are helping support operations compare channel-level resolution speed.

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

Return one row per `source_channel` with:

- `source_channel`
- `opened_tickets` (distinct tickets)
- `resolved_tickets_7d` (distinct tickets with at least one `resolved` update from opened date through opened date + 7 days)
- `resolution_rate_pct_7d` (`100 * resolved_tickets_7d / opened_tickets`, rounded to one decimal)

Use `left join` so tickets with no updates are still included.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q002_lower;` (see `scratchpad.sql`).
