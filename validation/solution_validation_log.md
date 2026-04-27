# Solution Validation Log

- Generated at: 2026-04-27T22:21:51.152220+00:00
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

## lower/q003_priority_mix_by_channel

- Database: `data\duckdb\q003_lower.duckdb`
- SQL file: `solutions\lower\q003_priority_mix_by_channel.sql`

- Statement 1: `3` rows

```text
source_channel, total_tickets, high_priority_tickets, high_priority_pct, priority_risk_band
chat, 194, 39, 20.1, medium_risk
email, 342, 51, 14.9, low_risk
phone, 124, 40, 32.3, high_risk
```

## lower/q004_carrier_on_time_delivery_basics

- Database: `data\duckdb\q004_lower.duckdb`
- SQL file: `solutions\lower\q004_carrier_on_time_delivery_basics.sql`

- Statement 1: `263` rows

```text
shipment_id, carrier, promised_date, first_delivered_date, days_late
shipment_00049, postal_economy, 2024-05-07, 2024-05-11, 4
shipment_00055, postal_economy, 2024-08-05, 2024-08-09, 4
shipment_00081, postal_economy, 2024-05-29, 2024-06-02, 4
shipment_00114, postal_economy, 2024-07-25, 2024-07-29, 4
shipment_00129, postal_economy, 2024-07-04, 2024-07-08, 4
... (258 more rows)
```

## lower/q005_inventory_snapshot_quality_checks

- Database: `data\duckdb\q005_lower.duckdb`
- SQL file: `solutions\lower\q005_inventory_snapshot_quality_checks.sql`

- Statement 1: `4` rows

```text
store_id, product_id, snapshot_date, duplicate_count
store_002, prod_b, 2024-08-10, 3
store_003, prod_d, 2024-08-12, 3
store_001, prod_c, 2024-08-04, 2
store_003, prod_a, 2024-08-08, 2
```

## lower/q006_refund_without_return

- Database: `data\duckdb\q006_lower.duckdb`
- SQL file: `solutions\lower\q006_refund_without_return.sql`

- Statement 1: `16` rows

```text
order_id, customer_id, order_date
order_00000, cust_001, 2024-09-01
order_00012, cust_013, 2024-09-13
order_00024, cust_025, 2024-09-04
order_00036, cust_037, 2024-09-16
order_00048, cust_004, 2024-09-07
... (11 more rows)
```

## lower/q007_trial_conversion_window_filter

- Database: `data\duckdb\q007_lower.duckdb`
- SQL file: `solutions\lower\q007_trial_conversion_window_filter.sql`

- Statement 1: `91` rows

```text
user_id, signup_date, subscription_start_date, days_to_convert
user_0000, 2024-10-01, 2024-10-01, 0
user_0001, 2024-10-02, 2024-10-09, 7
user_0003, 2024-10-04, 2024-10-07, 3
user_0005, 2024-10-06, 2024-10-06, 0
user_0006, 2024-10-07, 2024-10-14, 7
... (86 more rows)
```

## lower/q008_failed_logins_before_first_success

- Database: `data\duckdb\q008_lower.duckdb`
- SQL file: `solutions\lower\q008_failed_logins_before_first_success.sql`

- Statement 1: `37` rows

```text
user_id, first_success_time, failed_attempts_before_success
user_0000, 2024-11-01 08:03:00, 3
user_0004, 2024-11-01 08:48:00, 4
user_0005, 2024-11-01 08:58:00, 3
user_0009, 2024-11-01 09:43:00, 4
user_0010, 2024-11-01 09:53:00, 3
... (32 more rows)
```

## lower/q009_top_genres_with_watch_time_ties

- Database: `data\duckdb\q009_lower.duckdb`
- SQL file: `solutions\lower\q009_top_genres_with_watch_time_ties.sql`

- Statement 1: `45` rows

```text
user_id, genre, total_watch_minutes
user_0000, action, 10
user_0001, comedy, 14
user_0002, drama, 18
user_0003, documentary, 22
user_0004, action, 26
... (40 more rows)
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
2024-01-01, 19781.500, 521.000, 19260.500, 2.63
2024-02-01, 19295.500, 852.870, 18442.630, 4.42
2024-03-01, 18591.500, 1919.740, 16671.760, 10.33
2024-04-01, 19063.500, 2814.750, 16248.750, 14.77
2024-05-01, 19598.500, 952.990, 18645.510, 4.86
... (1 more rows)
```

## core/q004_renewal_outcome_classification

- Database: `data\duckdb\q004_core.duckdb`
- SQL file: `solutions\core\q004_renewal_outcome_classification.sql`

- Statement 1: `54` rows

```text
subscription_id, account_id, renewal_date, first_paid_invoice_date, renewal_outcome
sub_00013, acct_0013, 2024-11-02, 2024-11-12, renewed_late
sub_00014, acct_0014, 2024-11-03, None, not_renewed
sub_00015, acct_0015, 2024-11-04, 2024-11-04, renewed_on_time
sub_00016, acct_0016, 2024-11-05, 2024-11-07, renewed_on_time
sub_00017, acct_0017, 2024-11-06, 2024-11-16, renewed_late
... (49 more rows)
```

## core/q005_overlapping_subscription_periods_audit

- Database: `data\duckdb\q005_core.duckdb`
- SQL file: `solutions\core\q005_overlapping_subscription_periods_audit.sql`

- Statement 1: `4` rows

```text
account_id, subscription_id_a, subscription_id_b, overlap_start_date, overlap_end_date
acct_0007, sub_0007_ov1, sub_0007_ov2, 2024-03-20, 2024-04-15
acct_0021, sub_0021_ov1, sub_0021_ov2, 2024-02-15, 2024-02-28
acct_0044, sub_0044_ov1, sub_0044_ov2, 2024-05-15, 2024-07-20
acct_0069, sub_0069_ov1, sub_0069_ov2, 2024-06-30, 2024-06-30
```

## core/q006_top_genre_lexicographic_tie_break

- Database: `data\duckdb\q006_core.duckdb`
- SQL file: `solutions\core\q006_top_genre_lexicographic_tie_break.sql`

- Statement 1: `36` rows

```text
user_id, primary_genre, primary_genre_watch_minutes
acct_0000, action, 200
acct_0001, comedy, 201
acct_0002, drama, 202
acct_0003, documentary, 203
acct_0004, action, 204
... (31 more rows)
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
