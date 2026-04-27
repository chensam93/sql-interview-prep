# Q009 (Lower): Top genres with watch-time ties (fixed 30-day window)

## Scenario

You support a subscription streaming product. Analysts want a **per-user “best genre”** for a recent viewing window, based on **total watch minutes**.

Some users split time evenly across genres. For this task, **return every genre tied for #1** (do not pick a single winner).

## Window definition (fixed)

Use an **inclusive 30-day** window:

- `window_start = date '2026-03-29'`
- `window_end   = date '2026-04-27'`

Only count rows where `event_date` is between `window_start` and `window_end` (inclusive).

## Tables

### `playback_events`

| column | type | description |
| --- | --- | --- |
| `user_id` | `varchar` | viewer identifier |
| `genre` | `varchar` | genre label for the viewed title |
| `event_date` | `date` | day the watch minutes occurred |
| `watch_minutes` | `integer` | minutes watched (already aggregated per row) |

## Requirements

For each `user_id` who has **at least one in-window row**:

1. Sum `watch_minutes` by `user_id` and `genre` (in-window only).
2. Determine the **maximum** total watch minutes for that user.
3. Return **all genres** whose total equals that maximum (ties included).
4. Exclude users with **no** in-window rows.

## Output

Return one row per `(user_id, tied_genre)`:

| column | type |
| --- | --- |
| `user_id` | `varchar` |
| `genre` | `varchar` |
| `total_watch_minutes` | `integer` |

## Notes

- Ordering is not graded unless you choose to add an `order by` for readability.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q009_lower;` (see `scratchpad.sql`).
