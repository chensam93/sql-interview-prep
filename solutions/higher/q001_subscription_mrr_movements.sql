-- Q001 (Higher) Reference Solution: Subscription MRR Movements
-- Statement 1 expected result (exact, 6 rows):
-- snapshot_month, starting_mrr, new_mrr, expansion_mrr, contraction_mrr, churn_mrr, ending_mrr
-- 2024-01-01, 0.000, 25411.000, 0.000, 0.000, 0.000, 25411.000
-- 2024-02-01, 25411.000, 938.000, 1870.000, 1660.000, 1884.000, 24675.000
-- 2024-03-01, 24675.000, 1810.000, 1275.000, 1590.000, 2854.000, 23316.000
-- 2024-04-01, 23316.000, 1824.000, 2190.000, 1030.000, 1568.000, 24732.000
-- 2024-05-01, 24732.000, 1213.000, 1365.000, 1630.000, 2701.000, 22979.000
-- 2024-06-01, 22979.000, 1167.000, 1380.000, 1410.000, 2574.000, 21542.000
--
-- Statement 2 expected result shape: 30 rows.
-- Statement 2 expected output preview:
-- snapshot_month, account_id, net_mrr_change, change_rank
-- 2024-01-01, acct_0077, 339.000, 1
-- 2024-01-01, acct_0094, 339.000, 2
-- 2024-01-01, acct_0099, 339.000, 3
-- 2024-01-01, acct_0127, 339.000, 4
-- 2024-01-01, acct_0149, 339.000, 5

with account_monthly_mrr as (
    select
        subscription_snapshots.snapshot_month,
        subscription_snapshots.account_id,
        subscription_snapshots.mrr as current_mrr,
        coalesce(
            lag(subscription_snapshots.mrr) over (
                partition by subscription_snapshots.account_id
                order by subscription_snapshots.snapshot_month
            ),
            0
        ) as prior_mrr
    from subscription_snapshots
),
classified_mrr as (
    select
        account_monthly_mrr.snapshot_month,
        account_monthly_mrr.account_id,
        account_monthly_mrr.prior_mrr,
        account_monthly_mrr.current_mrr,
        case
            when account_monthly_mrr.prior_mrr = 0 and account_monthly_mrr.current_mrr > 0 then account_monthly_mrr.current_mrr
            else 0
        end as new_mrr,
        case
            when account_monthly_mrr.prior_mrr > 0 and account_monthly_mrr.current_mrr > account_monthly_mrr.prior_mrr
                then account_monthly_mrr.current_mrr - account_monthly_mrr.prior_mrr
            else 0
        end as expansion_mrr,
        case
            when account_monthly_mrr.prior_mrr > 0 and account_monthly_mrr.current_mrr < account_monthly_mrr.prior_mrr and account_monthly_mrr.current_mrr > 0
                then account_monthly_mrr.prior_mrr - account_monthly_mrr.current_mrr
            else 0
        end as contraction_mrr,
        case
            when account_monthly_mrr.prior_mrr > 0 and account_monthly_mrr.current_mrr = 0 then account_monthly_mrr.prior_mrr
            else 0
        end as churn_mrr
    from account_monthly_mrr
)
select
    classified_mrr.snapshot_month,
    sum(classified_mrr.prior_mrr) as starting_mrr,
    sum(classified_mrr.new_mrr) as new_mrr,
    sum(classified_mrr.expansion_mrr) as expansion_mrr,
    sum(classified_mrr.contraction_mrr) as contraction_mrr,
    sum(classified_mrr.churn_mrr) as churn_mrr,
    sum(classified_mrr.current_mrr) as ending_mrr
from classified_mrr
group by classified_mrr.snapshot_month
order by classified_mrr.snapshot_month;


with account_monthly_mrr as (
    select
        subscription_snapshots.snapshot_month,
        subscription_snapshots.account_id,
        subscription_snapshots.mrr as current_mrr,
        coalesce(
            lag(subscription_snapshots.mrr) over (
                partition by subscription_snapshots.account_id
                order by subscription_snapshots.snapshot_month
            ),
            0
        ) as prior_mrr
    from subscription_snapshots
),
net_changes as (
    select
        account_monthly_mrr.snapshot_month,
        account_monthly_mrr.account_id,
        account_monthly_mrr.current_mrr - account_monthly_mrr.prior_mrr as net_mrr_change
    from account_monthly_mrr
    where account_monthly_mrr.current_mrr - account_monthly_mrr.prior_mrr > 0
),
ranked_changes as (
    select
        net_changes.snapshot_month,
        net_changes.account_id,
        net_changes.net_mrr_change,
        row_number() over (
            partition by net_changes.snapshot_month
            order by
                net_changes.net_mrr_change desc,
                net_changes.account_id asc
        ) as change_rank
    from net_changes
)
select
    ranked_changes.snapshot_month,
    ranked_changes.account_id,
    ranked_changes.net_mrr_change,
    ranked_changes.change_rank
from ranked_changes
where ranked_changes.change_rank <= 5
order by
    ranked_changes.snapshot_month,
    ranked_changes.change_rank;
