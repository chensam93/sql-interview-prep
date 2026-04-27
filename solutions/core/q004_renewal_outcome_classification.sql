-- Q004 (Core) Reference Solution: Renewal Outcome Classification
-- Expected output (sample, first 5 rows):
-- subscription_id, account_id, renewal_date, first_paid_invoice_date, renewal_outcome
-- sub_00013, acct_0013, 2024-11-02, 2024-11-12, renewed_late
-- sub_00014, acct_0014, 2024-11-03, null, not_renewed
-- sub_00015, acct_0015, 2024-11-04, 2024-11-04, renewed_on_time
-- sub_00016, acct_0016, 2024-11-05, 2024-11-07, renewed_on_time
-- sub_00017, acct_0017, 2024-11-06, 2024-11-16, renewed_late

with november_active_subscriptions as (
    select
        subscriptions.subscription_id,
        subscriptions.account_id,
        subscriptions.renewal_date
    from subscriptions
    where subscriptions.status = 'active'
        and subscriptions.renewal_date between date '2024-11-01' and date '2024-11-30'
),
paid_invoice_candidates as (
    select
        november_active_subscriptions.subscription_id,
        min(invoices.invoice_date) as first_paid_invoice_date
    from november_active_subscriptions
    left join invoices
        on november_active_subscriptions.subscription_id = invoices.subscription_id
    where invoices.invoice_status = 'paid'
        and invoices.invoice_date >= november_active_subscriptions.renewal_date
    group by
        november_active_subscriptions.subscription_id
),
renewal_classification as (
    select
        november_active_subscriptions.subscription_id,
        november_active_subscriptions.account_id,
        november_active_subscriptions.renewal_date,
        paid_invoice_candidates.first_paid_invoice_date,
        case
            when paid_invoice_candidates.first_paid_invoice_date is null then 'not_renewed'
            when paid_invoice_candidates.first_paid_invoice_date <= november_active_subscriptions.renewal_date + interval '7 day'
                then 'renewed_on_time'
            else 'renewed_late'
        end as renewal_outcome
    from november_active_subscriptions
    left join paid_invoice_candidates
        on november_active_subscriptions.subscription_id = paid_invoice_candidates.subscription_id
)
select
    renewal_classification.subscription_id,
    renewal_classification.account_id,
    renewal_classification.renewal_date,
    renewal_classification.first_paid_invoice_date,
    renewal_classification.renewal_outcome
from renewal_classification
order by
    renewal_classification.subscription_id;
