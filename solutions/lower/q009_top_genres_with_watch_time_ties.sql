-- Q009 (Lower) Reference Solution: Top genres with watch-time ties (fixed 30-day window)
-- Expected output (sample, first 5 rows):
-- user_id, genre, total_watch_minutes
-- user_0000, action, 10
-- user_0001, comedy, 14
-- user_0002, drama, 18
-- user_0003, documentary, 22
-- user_0004, action, 26

with playback_in_window as (
    select
        playback_events.user_id,
        playback_events.genre,
        playback_events.watch_minutes
    from playback_events
    where playback_events.event_date between date '2026-03-29' and date '2026-04-27'
),
genre_totals as (
    select
        playback_in_window.user_id,
        playback_in_window.genre,
        sum(playback_in_window.watch_minutes) as total_watch_minutes
    from playback_in_window
    group by
        playback_in_window.user_id,
        playback_in_window.genre
),
best_total as (
    select
        genre_totals.user_id,
        max(genre_totals.total_watch_minutes) as max_total_watch_minutes
    from genre_totals
    group by
        genre_totals.user_id
)
select
    genre_totals.user_id,
    genre_totals.genre,
    genre_totals.total_watch_minutes
from genre_totals
inner join best_total
    on genre_totals.user_id = best_total.user_id
    and genre_totals.total_watch_minutes = best_total.max_total_watch_minutes
order by
    genre_totals.user_id,
    genre_totals.genre;
