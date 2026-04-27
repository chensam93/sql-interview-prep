-- Q007 (Lower) Reference Solution: Trial Conversion Window Filter
-- Expected output (sample, first 5 rows):
-- user_id, signup_date, subscription_start_date, days_to_convert
-- user_0000, 2024-10-01, 2024-10-01, 0
-- user_0001, 2024-10-02, 2024-10-09, 7
-- user_0003, 2024-10-04, 2024-10-07, 3
-- user_0005, 2024-10-06, 2024-10-06, 0
-- user_0006, 2024-10-07, 2024-10-14, 7

with trial_to_subscription as (
    select
        trial_signups.user_id,
        trial_signups.signup_date,
        subscriptions.subscription_start_date
    from trial_signups
    inner join subscriptions
        on trial_signups.user_id = subscriptions.user_id
),
conversion_window_filter as (
    select
        trial_to_subscription.user_id,
        trial_to_subscription.signup_date,
        trial_to_subscription.subscription_start_date,
        trial_to_subscription.subscription_start_date - trial_to_subscription.signup_date as days_to_convert
    from trial_to_subscription
    where trial_to_subscription.subscription_start_date
        between trial_to_subscription.signup_date
            and trial_to_subscription.signup_date + interval '7 day'
)
select
    conversion_window_filter.user_id,
    conversion_window_filter.signup_date,
    conversion_window_filter.subscription_start_date,
    conversion_window_filter.days_to_convert
from conversion_window_filter
order by
    conversion_window_filter.user_id;
