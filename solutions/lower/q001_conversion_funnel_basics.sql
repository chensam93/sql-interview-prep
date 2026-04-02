-- Q001 (Lower) Reference Solution: Conversion Funnel Basics

with signups_with_events as (
    select
        signups.user_id,
        signups.signup_date,
        date_trunc('week', signups.signup_date)::date as signup_week,
        signups.acquisition_channel,
        max(
            case
                when events.event_name = 'profile_complete'
                    and events.event_date <= signups.signup_date + interval '14 day'
                then 1
                else 0
            end
        ) as has_profile_complete,
        max(
            case
                when events.event_name = 'first_purchase'
                    and events.event_date <= signups.signup_date + interval '30 day'
                then 1
                else 0
            end
        ) as has_purchase
    from signups
    left join events
        on events.user_id = signups.user_id
       and events.event_date >= signups.signup_date
    group by
        signups.user_id,
        signups.signup_date,
        date_trunc('week', signups.signup_date)::date,
        signups.acquisition_channel
),
weekly_funnel as (
    select
        signup_week,
        count(*) as signed_up_users,
        sum(has_profile_complete) as profile_completed_users,
        sum(has_purchase) as purchased_users
    from signups_with_events
    group by signup_week
)
select
    weekly_funnel.signup_week,
    weekly_funnel.signed_up_users,
    weekly_funnel.profile_completed_users,
    weekly_funnel.purchased_users,
    round(100.0 * weekly_funnel.profile_completed_users / weekly_funnel.signed_up_users, 1) as profile_completion_rate_pct,
    round(100.0 * weekly_funnel.purchased_users / weekly_funnel.signed_up_users, 1) as purchase_rate_pct
from weekly_funnel
order by weekly_funnel.signup_week;


with signups_with_events as (
    select
        signups.user_id,
        date_trunc('week', signups.signup_date)::date as signup_week,
        signups.acquisition_channel,
        max(
            case
                when events.event_name = 'first_purchase'
                    and events.event_date <= signups.signup_date + interval '30 day'
                then 1
                else 0
            end
        ) as has_purchase
    from signups
    left join events
        on events.user_id = signups.user_id
       and events.event_date >= signups.signup_date
    group by
        signups.user_id,
        date_trunc('week', signups.signup_date)::date,
        signups.acquisition_channel
),
channel_purchases as (
    select
        signup_week,
        acquisition_channel,
        sum(has_purchase) as purchased_users
    from signups_with_events
    group by
        signup_week,
        acquisition_channel
),
ranked_channels as (
    select
        channel_purchases.signup_week,
        channel_purchases.acquisition_channel,
        channel_purchases.purchased_users,
        row_number() over (
            partition by channel_purchases.signup_week
            order by
                channel_purchases.purchased_users desc,
                channel_purchases.acquisition_channel asc
        ) as channel_rank
    from channel_purchases
)
select
    ranked_channels.signup_week,
    ranked_channels.acquisition_channel,
    ranked_channels.purchased_users
from ranked_channels
where ranked_channels.channel_rank = 1
order by ranked_channels.signup_week;
