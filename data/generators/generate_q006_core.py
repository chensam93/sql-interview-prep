"""
Generate sample data for Q006 (Core): Top genre with lexicographic tie-break.
Creates: data/duckdb/q006_core.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q006_core.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists playback_events")

window_end = date(2026, 4, 27)
window_start = window_end - timedelta(days=29)

playback_events: list[tuple[str, str, date, int]] = []

# Background users: deterministic totals with a unique max genre per user.
for user_index in range(35):
    user_id = f"acct_{user_index:04d}"
    top_genre = ["action", "comedy", "drama", "documentary"][user_index % 4]
    other_genre = ["kids", "news", "sports", "reality"][user_index % 4]

    day_a = window_start + timedelta(days=(user_index % 18))
    day_b = window_start + timedelta(days=((user_index + 5) % 18))

    top_minutes = 200 + user_index
    other_minutes = 50 + (user_index % 6)

    playback_events.append((user_id, top_genre, day_a, top_minutes))
    playback_events.append((user_id, other_genre, day_b, other_minutes))

# Explicit tie-break case: equal totals, winner must be lexicographically smallest genre name.
playback_events.extend(
    [
        ("acct_tie_break", "zebra", window_start + timedelta(days=1), 100),
        ("acct_tie_break", "alpha", window_start + timedelta(days=2), 100),
        ("acct_tie_break", "mango", window_start + timedelta(days=3), 25),
    ]
)

connection.execute(
    """
    create table playback_events (
        user_id varchar,
        genre varchar,
        event_date date,
        watch_minutes integer
    )
    """
)

connection.executemany("insert into playback_events values (?, ?, ?, ?)", playback_events)

print(f"Created {database_path}")
connection.close()
