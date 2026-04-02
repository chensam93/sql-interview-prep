# Solution Validation Log

- Generated at: 2026-04-02T11:14:13.182282+00:00
- Scope: execute each reference solution statement against its bucket-specific DuckDB file.
- Assumption (lower): milestone events counted once per user using `max(case ...)` flags.
- Assumption (core): rolling average uses available history for early months (fewer than 3 rows).
- Assumption (higher): missing prior month mrr is treated as `0` via `lag(..., default 0)` logic.

## lower/q001_conversion_funnel_basics

- Database: `data\duckdb\q001_lower.duckdb`
- SQL file: `solutions\lower\q001_conversion_funnel_basics.sql`

- Statement 1: `13` rows

```text
signup_week, signed_up_users, profile_completed_users, purchased_users, profile_completion_rate_pct, purchase_rate_pct
2024-01-01, 71, 52, 26, 73.2, 36.6
2024-01-08, 62, 50, 18, 80.6, 29.0
2024-01-15, 72, 48, 29, 66.7, 40.3
2024-01-22, 79, 58, 23, 73.4, 29.1
2024-01-29, 74, 53, 20, 71.6, 27.0
... (8 more rows)
```

- Statement 2: `13` rows

```text
signup_week, acquisition_channel, purchased_users
2024-01-01, organic, 13
2024-01-08, paid_search, 8
2024-01-15, organic, 10
2024-01-22, paid_search, 8
2024-01-29, organic, 9
... (8 more rows)
```

## core/q001_monthly_revenue_trends

- Database: `data\duckdb\q001_core.duckdb`
- SQL file: `solutions\core\q001_monthly_revenue_trends.sql`

- Statement 1: `6` rows

```text
order_month, monthly_revenue, three_month_rolling_avg_revenue
2024-01-01, 36337.000, 36337.0
2024-02-01, 24384.000, 30360.5
2024-03-01, 33623.000, 31448.0
2024-04-01, 21923.000, 26643.333333333332
2024-05-01, 31930.000, 29158.666666666668
... (1 more rows)
```

- Statement 2: `6` rows

```text
order_month, product_id, product_revenue
2024-01-01, prod_e, 15496.000
2024-02-01, prod_e, 8021.000
2024-03-01, prod_e, 16538.000
2024-04-01, prod_e, 7361.000
2024-05-01, prod_e, 12393.000
... (1 more rows)
```

## higher/q001_subscription_mrr_movements

- Database: `data\duckdb\q001_higher.duckdb`
- SQL file: `solutions\higher\q001_subscription_mrr_movements.sql`

- Statement 1: `6` rows

```text
snapshot_month, starting_mrr, new_mrr, expansion_mrr, contraction_mrr, churn_mrr, ending_mrr
2024-01-01, 0.000, 25411.000, 0.000, 0.000, 0.000, 25411.000
2024-02-01, 25411.000, 938.000, 1870.000, 1660.000, 1884.000, 24675.000
2024-03-01, 24675.000, 1810.000, 1275.000, 1590.000, 2854.000, 23316.000
2024-04-01, 23316.000, 1824.000, 2190.000, 1030.000, 1568.000, 24732.000
2024-05-01, 24732.000, 1213.000, 1365.000, 1630.000, 2701.000, 22979.000
... (1 more rows)
```

- Statement 2: `30` rows

```text
snapshot_month, account_id, net_mrr_change, change_rank
2024-01-01, acct_0077, 339.000, 1
2024-01-01, acct_0094, 339.000, 2
2024-01-01, acct_0099, 339.000, 3
2024-01-01, acct_0127, 339.000, 4
2024-01-01, acct_0149, 339.000, 5
... (25 more rows)
```

## Invariant Checks

- Core: Distinct months in raw data: 6
- Lower: Weeks with purchased_users > signed_up_users: 0
- Higher: Months violating MRR bridge equation: 0
