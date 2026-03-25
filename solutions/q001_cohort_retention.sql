-- Q001 Reference Solution: Cohort Retention Analysis
-- -----------------------------------------------------------------------------
-- PART A: weekly cohorts x D1 / D7 / D30 retention
-- -----------------------------------------------------------------------------

with cohort_users as (
    select
        users.user_id,
        users.signup_date,
        date_trunc('week', users.signup_date) as cohort_week
    from users
),
day_1_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '1 day'
),
day_7_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '7 days'
),
day_30_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '30 days'
),
cohort_retention as (
    select
        cohort_users.cohort_week,
        count(distinct cohort_users.user_id) as cohort_size,
        count(distinct day_1_active_users.user_id) as retained_d1,
        count(distinct day_7_active_users.user_id) as retained_d7,
        count(distinct day_30_active_users.user_id) as retained_d30,
        round(
            100.0 * count(distinct day_1_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d1,
        round(
            100.0 * count(distinct day_7_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d7,
        round(
            100.0 * count(distinct day_30_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d30
    from cohort_users
    left join day_1_active_users
        on day_1_active_users.user_id = cohort_users.user_id
    left join day_7_active_users
        on day_7_active_users.user_id = cohort_users.user_id
    left join day_30_active_users
        on day_30_active_users.user_id = cohort_users.user_id
    group by
        cohort_users.cohort_week
)

select
    cohort_retention.cohort_week,
    cohort_retention.cohort_size,
    cohort_retention.retained_d1,
    cohort_retention.retained_d7,
    cohort_retention.retained_d30,
    cohort_retention.retention_rate_d1,
    cohort_retention.retention_rate_d7,
    cohort_retention.retention_rate_d30
from cohort_retention
order by cohort_retention.cohort_week;


-- -----------------------------------------------------------------------------
-- PART B: break out by plan_type
-- -----------------------------------------------------------------------------

with cohort_users as (
    select
        users.user_id,
        users.signup_date,
        users.plan_type,
        date_trunc('week', users.signup_date) as cohort_week
    from users
),
day_1_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '1 day'
),
day_7_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '7 days'
),
day_30_active_users as (
    select distinct
        cohort_users.user_id
    from cohort_users
    inner join activity
        on activity.user_id = cohort_users.user_id
       and activity.activity_date = cohort_users.signup_date + interval '30 days'
),
cohort_retention_by_plan_type as (
    select
        cohort_users.cohort_week,
        cohort_users.plan_type,
        count(distinct cohort_users.user_id) as cohort_size,
        count(distinct day_1_active_users.user_id) as retained_d1,
        count(distinct day_7_active_users.user_id) as retained_d7,
        count(distinct day_30_active_users.user_id) as retained_d30,
        round(
            100.0 * count(distinct day_1_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d1,
        round(
            100.0 * count(distinct day_7_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d7,
        round(
            100.0 * count(distinct day_30_active_users.user_id) / count(distinct cohort_users.user_id),
            1
        ) as retention_rate_d30
    from cohort_users
    left join day_1_active_users
        on day_1_active_users.user_id = cohort_users.user_id
    left join day_7_active_users
        on day_7_active_users.user_id = cohort_users.user_id
    left join day_30_active_users
        on day_30_active_users.user_id = cohort_users.user_id
    group by
        cohort_users.cohort_week,
        cohort_users.plan_type
)

select
    cohort_retention_by_plan_type.cohort_week,
    cohort_retention_by_plan_type.plan_type,
    cohort_retention_by_plan_type.cohort_size,
    cohort_retention_by_plan_type.retained_d1,
    cohort_retention_by_plan_type.retained_d7,
    cohort_retention_by_plan_type.retained_d30,
    cohort_retention_by_plan_type.retention_rate_d1,
    cohort_retention_by_plan_type.retention_rate_d7,
    cohort_retention_by_plan_type.retention_rate_d30
from cohort_retention_by_plan_type
order by
    cohort_retention_by_plan_type.cohort_week,
    cohort_retention_by_plan_type.plan_type;


-- -----------------------------------------------------------------------------
-- PART C discussion notes
-- -----------------------------------------------------------------------------

-- Immature cohorts: filter out cohorts where signup_date > current_date - 30
-- (they cannot have hit D30 yet). Otherwise recent cohorts look artificially
-- weak. Flag immature cohorts or exclude them from D30 reporting.

-- Duplicate activity rows: distinct user_id in each milestone CTE ensures
-- retention is measured as "was active" rather than "number of activities".

-- dbt model design:
--   grain: cohort_week (or cohort_week + plan_type for Part B)
--   full refresh is safe for this dataset because retention windows are fixed.
--   incremental can work, but requires reprocessing recent cohorts until D30
--   is finalized.
