"""
Generate sample data for Q009 (Lower): Top tied genres in a fixed watch window.
Creates: data/duckdb/q009_lower.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q009_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists playback_events")

window_end = date(2026, 4, 27)
window_start = window_end - timedelta(days=29)

playback_events: list[tuple[str, str, date, int]] = []

# Background users: deterministic, intentionally no cross-genre ties at the top.
for user_index in range(40):
    user_id = f"user_{user_index:04d}"
    primary_genre = ["action", "comedy", "drama", "documentary"][user_index % 4]
    secondary_genre = ["kids", "news", "sports", "reality"][user_index % 4]

    day_a = window_start + timedelta(days=(user_index % 20))
    day_b = window_start + timedelta(days=((user_index + 7) % 20))

    primary_minutes = 10 + (user_index * 3) + (user_index % 5)
    secondary_minutes = 2 + (user_index % 4)

    playback_events.append((user_id, primary_genre, day_a, primary_minutes))
    playback_events.append((user_id, secondary_genre, day_b, secondary_minutes))

# Explicit tie cases (should return multiple rows for the same user).
playback_events.extend(
    [
        ("user_tie_2way", "comedy", window_start + timedelta(days=1), 120),
        ("user_tie_2way", "drama", window_start + timedelta(days=2), 120),
        ("user_tie_2way", "news", window_start + timedelta(days=3), 40),
        ("user_tie_3way", "news", window_start + timedelta(days=4), 60),
        ("user_tie_3way", "sports", window_start + timedelta(days=5), 60),
        ("user_tie_3way", "kids", window_start + timedelta(days=6), 60),
        ("user_tie_3way", "reality", window_start + timedelta(days=7), 10),
    ]
)

# User with only out-of-window viewing (should not appear in results).
playback_events.append(("user_only_outside_window", "action", window_start - timedelta(days=3), 999))

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
