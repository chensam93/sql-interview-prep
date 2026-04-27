# Interview snippets — example (committed)

Copy this file to `interview_snippets.local.md` (gitignored). Keep entries short and anonymized.

**Habit:** append a new `## YYYY-MM-DD — short title` section whenever you have a fresh example. One entry per session is enough; skip days with nothing new.

## Optional index (at top of your local file)

| date | title | repo |
| --- | --- | --- |
| YYYY-MM-DD | one-line label | `questions/...` or blank |

## Entry template

- **Date**:
- **Role level** (lower / core / higher guess):
- **Grain**:
- **Tables implied** (even if the interviewer only described logs):
- **Time rules**:
- **Correctness traps** (ties, duplicates, nulls, late events):
- **Desired output** (one row vs many rows):
- **Repo translation** (question path or “not yet modeled”):

## Illustrative entry (fictional company)

- **Date**: (example)
- **Role level**: lower vs core depends on tie policy
- **Grain**: user
- **Tables implied**: per-user genre watch totals inside a fixed calendar window
- **Time rules**: fixed window end date in the prompt (avoid rolling `current_date`)
- **Correctness traps**: multiple genres tie for max watch minutes
- **Desired output**:
  - preserve ties → multiple rows per user
  - single label → explicit tie-break rule (e.g. lexicographic genre name)
- **Repo translation**: see `questions/lower/q009_top_genres_with_watch_time_ties.md` and `questions/core/q006_top_genre_lexicographic_tie_break.md`
