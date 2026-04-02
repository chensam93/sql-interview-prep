# Q001 (Higher) - Subscription MRR Movements

**Level:** Higher (harder than typical senior AE loops)  
**Concepts tested:** ctes, windows, lifecycle classification, monthly rollforwards

---

## Scenario

Finance wants a monthly MRR bridge that explains movement by type.

You have one table:

### `subscription_snapshots`
| column | type | description |
|--------|------|-------------|
| `snapshot_month` | date | month start date |
| `account_id` | varchar | customer account id |
| `mrr` | numeric | end-of-month mrr for that account/month |

---

## Questions

### Query 1
Build one row per month with:
- `snapshot_month`
- `starting_mrr`
- `new_mrr`
- `expansion_mrr`
- `contraction_mrr`
- `churn_mrr`
- `ending_mrr`

### Query 2
For each month, return the top 5 accounts by positive net mrr change (`current_mrr - prior_mrr`), excluding non-positive change.

Tie-breaker: `account_id` ascending.

---

## Data

Connect to: `data/duckdb/workspace_verify.duckdb` and run `USE workspace_db.q001_higher;` (see `scratchpad.sql`).
