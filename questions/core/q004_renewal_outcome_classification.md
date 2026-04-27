# Q004 (Core) - Renewal Outcome Classification

**Level:** Core (mid + senior blend)  
**Concepts tested:** first-event logic, conditional classification, joins, date-window checks

---

## Scenario

Revenue operations wants to classify upcoming renewals based on payment timing.

You have three tables:

### `accounts`
| column | type | description |
|--------|------|-------------|
| `account_id` | varchar | account identifier |
| `segment` | varchar | account segment (`smb`, `mid_market`, `enterprise`) |

### `subscriptions`
| column | type | description |
|--------|------|-------------|
| `subscription_id` | varchar | subscription identifier |
| `account_id` | varchar | foreign key to accounts |
| `start_date` | date | subscription start date |
| `renewal_date` | date | renewal due date |
| `status` | varchar | subscription status (`active`, `cancelled`) |

### `invoices`
| column | type | description |
|--------|------|-------------|
| `invoice_id` | varchar | invoice identifier |
| `subscription_id` | varchar | foreign key to subscriptions |
| `invoice_date` | date | invoice date |
| `amount` | numeric | invoice amount |
| `invoice_status` | varchar | invoice status (`paid`, `failed`, `void`) |

---

## Question

For **active** subscriptions with `renewal_date` in November 2024 (`2024-11-01` to `2024-11-30`), return:

- `subscription_id`
- `account_id`
- `renewal_date`
- `first_paid_invoice_date` (first `paid` invoice on or after `renewal_date`; null if none)
- `renewal_outcome`:
  - `renewed_on_time` if `first_paid_invoice_date <= renewal_date + 7 days`
  - `renewed_late` if `first_paid_invoice_date > renewal_date + 7 days`
  - `not_renewed` if `first_paid_invoice_date` is null

Order by `subscription_id`.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q004_core;` (see `scratchpad.sql`).
