-- Q005 (Core) Reference Solution: Overlapping Subscription Periods Audit
-- Expected result (exact, 4 rows):
-- account_id, subscription_id_a, subscription_id_b, overlap_start_date, overlap_end_date
-- acct_0007, sub_0007_ov1, sub_0007_ov2, 2024-03-20, 2024-04-15
-- acct_0021, sub_0021_ov1, sub_0021_ov2, 2024-02-15, 2024-02-28
-- acct_0044, sub_0044_ov1, sub_0044_ov2, 2024-05-15, 2024-07-20
-- acct_0069, sub_0069_ov1, sub_0069_ov2, 2024-06-30, 2024-06-30

with subscription_pairs as (
    select
        subscriptions_a.account_id,
        subscriptions_a.subscription_id as subscription_id_a,
        subscriptions_b.subscription_id as subscription_id_b,
        greatest(subscriptions_a.start_date, subscriptions_b.start_date) as overlap_start_date,
        least(subscriptions_a.end_date, subscriptions_b.end_date) as overlap_end_date
    from account_subscriptions as subscriptions_a
    inner join account_subscriptions as subscriptions_b
        on subscriptions_a.account_id = subscriptions_b.account_id
    where subscriptions_a.subscription_id < subscriptions_b.subscription_id
),
overlapping_pairs as (
    select
        subscription_pairs.account_id,
        subscription_pairs.subscription_id_a,
        subscription_pairs.subscription_id_b,
        subscription_pairs.overlap_start_date,
        subscription_pairs.overlap_end_date
    from subscription_pairs
    where subscription_pairs.overlap_start_date <= subscription_pairs.overlap_end_date
)
select
    overlapping_pairs.account_id,
    overlapping_pairs.subscription_id_a,
    overlapping_pairs.subscription_id_b,
    overlapping_pairs.overlap_start_date,
    overlapping_pairs.overlap_end_date
from overlapping_pairs
order by
    overlapping_pairs.account_id,
    overlapping_pairs.subscription_id_a,
    overlapping_pairs.subscription_id_b;
