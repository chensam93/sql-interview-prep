# Q003 (Lower) - Priority Mix by Channel

**Level:** Lower (entry to early-career analytics engineering)  
**Concepts tested:** conditional aggregation, grouped counts, case statements, basic percentages

---

## Scenario

You are helping support operations understand the ticket mix by intake channel.

You have one table:

### `tickets`
| column | type | description |
|--------|------|-------------|
| `ticket_id` | varchar | unique ticket identifier |
| `opened_date` | date | when the ticket was opened |
| `priority` | varchar | `low`, `medium`, `high` |
| `source_channel` | varchar | `email`, `chat`, `phone` |

---

## Question

Return one row per `source_channel` with:

- `source_channel`
- `total_tickets` (distinct tickets)
- `high_priority_tickets` (distinct tickets where `priority = 'high'`)
- `high_priority_pct` (`100 * high_priority_tickets / total_tickets`, rounded to one decimal)
- `priority_risk_band`:
  - `high_risk` when `high_priority_pct >= 30`
  - `medium_risk` when `high_priority_pct >= 15` and `< 30`
  - `low_risk` otherwise

Order by `source_channel`.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q003_lower;` (see `scratchpad.sql`).
