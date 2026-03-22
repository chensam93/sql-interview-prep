-- Q001 Reference Solution: Cohort Retention Analysis
-- ─────────────────────────────────────────────────────────────────────────────
-- PART A: weekly cohorts × D1 / D7 / D30 retention
-- ─────────────────────────────────────────────────────────────────────────────

with cohorts as (
    select
        user_id,
        signup_date,
        date_trunc('week', signup_date) as cohort_week
    from users
),

-- one sub-join per milestone keeps the logic explicit and easy to audit
d1 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '1 day'
),

d7 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '7 days'
),

d30 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '30 days'
),

final as (
    select
        c.cohort_week,
        count(distinct c.user_id)                                    as cohort_size,
        count(distinct d1.user_id)                                   as retained_d1,
        count(distinct d7.user_id)                                   as retained_d7,
        count(distinct d30.user_id)                                  as retained_d30,
        round(100.0 * count(distinct d1.user_id)  / count(distinct c.user_id), 1) as retention_rate_d1,
        round(100.0 * count(distinct d7.user_id)  / count(distinct c.user_id), 1) as retention_rate_d7,
        round(100.0 * count(distinct d30.user_id) / count(distinct c.user_id), 1) as retention_rate_d30
    from cohorts c
    left join d1  on d1.user_id  = c.user_id
    left join d7  on d7.user_id  = c.user_id
    left join d30 on d30.user_id = c.user_id
    group by c.cohort_week
    order by c.cohort_week
)

select * from final;


-- ─────────────────────────────────────────────────────────────────────────────
-- PART B: break out by plan_type
-- ─────────────────────────────────────────────────────────────────────────────

with cohorts as (
    select
        user_id,
        signup_date,
        plan_type,
        date_trunc('week', signup_date) as cohort_week
    from users
),

d1 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '1 day'
),

d7 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '7 days'
),

d30 as (
    select distinct c.user_id
    from cohorts c
    inner join activity a
        on  a.user_id       = c.user_id
        and a.activity_date = c.signup_date + interval '30 days'
),

final as (
    select
        c.cohort_week,
        c.plan_type,
        count(distinct c.user_id)                                    as cohort_size,
        count(distinct d1.user_id)                                   as retained_d1,
        count(distinct d7.user_id)                                   as retained_d7,
        count(distinct d30.user_id)                                  as retained_d30,
        round(100.0 * count(distinct d1.user_id)  / count(distinct c.user_id), 1) as retention_rate_d1,
        round(100.0 * count(distinct d7.user_id)  / count(distinct c.user_id), 1) as retention_rate_d7,
        round(100.0 * count(distinct d30.user_id) / count(distinct c.user_id), 1) as retention_rate_d30
    from cohorts c
    left join d1  on d1.user_id  = c.user_id
    left join d7  on d7.user_id  = c.user_id
    left join d30 on d30.user_id = c.user_id
    group by c.cohort_week, c.plan_type
    order by c.cohort_week, c.plan_type
)

select * from final;


-- ─────────────────────────────────────────────────────────────────────────────
-- PART C discussion notes
-- ─────────────────────────────────────────────────────────────────────────────

-- Immature cohorts: filter out cohorts where signup_date > current_date - 30
-- (they can't have hit D30 yet). Otherwise you'd show 0% retention for recent
-- cohorts and mislead stakeholders. Flag immature cohorts or exclude them.

-- Duplicate activity rows: DISTINCT on user_id inside each milestone CTE
-- handles this. The question is about *whether* a user was active, not
-- how many times. Using COUNT(DISTINCT) in the outer group-by also works.

-- dbt model design:
--   grain: cohort_week (or cohort_week + plan_type for Part B)
--   full refresh is safe here — the dataset is bounded by signup dates and
--   the retention windows are fixed offsets (D1, D7, D30). An incremental
--   approach is tricky because a row's D30 retention value can only be
--   finalized 30 days after signup; you'd need to re-process recent cohorts.
--   Simpler to do full refresh unless the dataset is huge.
