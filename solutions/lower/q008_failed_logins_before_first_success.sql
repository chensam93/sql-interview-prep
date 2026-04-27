-- Q008 (Lower) Reference Solution: Failed Logins Before First Success
-- Expected output (sample, first 5 rows):
-- user_id, first_success_time, failed_attempts_before_success
-- user_0000, 2024-11-01 08:03:00, 3
-- user_0004, 2024-11-01 08:48:00, 4
-- user_0005, 2024-11-01 08:58:00, 3
-- user_0009, 2024-11-01 09:43:00, 4
-- user_0010, 2024-11-01 09:53:00, 3

with first_success_events as (
    select
        auth_events.user_id,
        min(auth_events.event_time) as first_success_time
    from auth_events
    where auth_events.event_type = 'successful_login'
    group by
        auth_events.user_id
),
failed_before_success as (
    select
        first_success_events.user_id,
        first_success_events.first_success_time,
        count(*) as failed_attempts_before_success
    from first_success_events
    inner join auth_events
        on first_success_events.user_id = auth_events.user_id
    where auth_events.event_type = 'failed_login'
        and auth_events.event_time < first_success_events.first_success_time
    group by
        first_success_events.user_id,
        first_success_events.first_success_time
)
select
    failed_before_success.user_id,
    failed_before_success.first_success_time,
    failed_before_success.failed_attempts_before_success
from failed_before_success
where failed_before_success.failed_attempts_before_success >= 3
order by
    failed_before_success.user_id;
