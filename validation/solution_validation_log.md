# Solution Validation Log

- Generated at: 2026-04-26T04:27:30.947928+00:00
- Scope: execute each reference solution statement against its bucket-specific DuckDB file.
- Assumption (lower): ticket resolution counted once per ticket using `max(case ...)` flags.
- Assumption (core): rolling average uses available history for early months (fewer than 3 rows).
- Assumption (core q002): prior-month channel revenue defaults to `0` when missing for MoM delta.
- Assumption (higher): missing prior month mrr is treated as `0` via `lag(..., default 0)` logic.

## lower/q001_conversion_funnel_basics

- Database: `data\duckdb\q001_lower.duckdb`
- SQL file: `solutions\lower\q001_conversion_funnel_basics.sql`

- Statement 1: `42` rows

```text
opened_week, priority, opened_tickets, resolved_tickets_3d, unresolved_tickets_3d, resolution_rate_pct_3d, resolution_band
2024-01-29, high, 11, 4, 7, 36.4, weak
2024-01-29, low, 19, 4, 15, 21.1, weak
2024-01-29, medium, 7, 3, 4, 42.9, ok
2024-02-05, high, 7, 4, 3, 57.1, ok
2024-02-05, low, 25, 9, 16, 36.0, weak
... (37 more rows)
```

## lower/q002_resolution_rate_by_channel

- Database: `data\duckdb\q002_lower.duckdb`
- SQL file: `solutions\lower\q002_resolution_rate_by_channel.sql`

- Statement 1: `3` rows

```text
source_channel, opened_tickets, resolved_tickets_7d, resolution_rate_pct_7d
chat, 224, 116, 51.8
email, 371, 150, 40.4
phone, 125, 55, 44.0
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

## core/q002_channel_customer_mix

- Database: `data\duckdb\q002_core.duckdb`
- SQL file: `solutions\core\q002_channel_customer_mix.sql`

- Statement 1: `36` rows

```text
order_month, channel, gross_revenue, new_customer_revenue, returning_customer_revenue, returning_revenue_share_pct
2024-01-01, affiliate, 3201.000, 3201.000, 0.000, 0.0
2024-01-01, email, 10160.000, 10160.000, 0.000, 0.0
2024-01-01, organic, 17587.000, 17587.000, 0.000, 0.0
2024-01-01, paid_search, 12193.000, 12193.000, 0.000, 0.0
2024-02-01, affiliate, 6051.000, 4127.000, 1924.000, 31.8
... (31 more rows)
```

- Statement 2: `9` rows

```text
order_month, channel, gross_revenue, mom_revenue_delta
2024-01-01, organic, 17587.000, 17587.000
2024-02-01, affiliate, 6051.000, 2850.000
2024-03-01, paid_search, 16753.000, 7030.000
2024-04-01, organic, 18148.000, 5384.000
2024-05-01, email, 13472.000, 5756.000
... (4 more rows)
```

## core/q003_monthly_net_after_returns

- Database: `data\duckdb\q003_core.duckdb`
- SQL file: `solutions\core\q003_monthly_net_after_returns.sql`

- Statement 1: `6` rows

```text
report_month, gross_revenue, refund_amount, net_revenue, refund_pct_of_gross
2024-01-01, 19781.500, 432.500, 19349.000, 2.19
2024-02-01, 19295.500, 1201.760, 18093.740, 6.23
2024-03-01, 18591.500, 1852.880, 16738.620, 9.97
2024-04-01, 19063.500, 2084.380, 16979.120, 10.93
2024-05-01, 19598.500, 1674.760, 17923.740, 8.55
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
- Lower: Weeks with resolved_tickets_3d > opened_tickets: 0
- Higher: Months violating MRR bridge equation: 0
