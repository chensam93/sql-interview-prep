# Q006 (Core): Top genre by watch minutes with a deterministic tie-break

## Scenario

Product wants a **single “primary genre”** per user for a fixed viewing window, based on **total watch minutes**.

Watch totals sometimes tie across genres. Marketing needs a **deterministic** rule so exports are stable.

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
2. Pick the genre with the **largest** total watch minutes.
3. If multiple genres tie for the largest total, choose the genre with the **smallest genre name in lexicographic (alphabetical) order** (standard string ordering for `varchar`).

Return **exactly one row per qualifying user**.

## Output

| column | type |
| --- | --- |
| `user_id` | `varchar` |
| `primary_genre` | `varchar` |
| `primary_genre_watch_minutes` | `integer` |

## Notes

- Ordering is not graded unless you add an `order by` for readability.

---

## Data

Connect to: `data/duckdb/workspace_build.duckdb` and run `USE workspace_db.q006_core;` (see `scratchpad.sql`).
