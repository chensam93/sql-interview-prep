-- Q006 (Core) Reference Solution: Top genre with lexicographic tie-break (fixed 30-day window)
-- Expected output (sample, first 5 rows):
-- user_id, primary_genre, primary_genre_watch_minutes
-- acct_0000, action, 200
-- acct_0001, comedy, 201
-- acct_0002, drama, 202
-- acct_0003, documentary, 203
-- acct_0004, action, 204

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
ranked_genres as (
    select
        genre_totals.user_id,
        genre_totals.genre,
        genre_totals.total_watch_minutes,
        row_number() over (
            partition by genre_totals.user_id
            order by
                genre_totals.total_watch_minutes desc,
                genre_totals.genre asc
        ) as genre_rank
    from genre_totals
),
top_genre as (
    select
        ranked_genres.user_id,
        ranked_genres.genre as primary_genre,
        ranked_genres.total_watch_minutes as primary_genre_watch_minutes
    from ranked_genres
    where ranked_genres.genre_rank = 1
)
select
    top_genre.user_id,
    top_genre.primary_genre,
    top_genre.primary_genre_watch_minutes
from top_genre
order by
    top_genre.user_id;
