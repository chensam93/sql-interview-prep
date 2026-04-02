-- Q001 (Higher) Reference Solution: Subscription MRR Movements

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
