# SQL Interview Prep

A live, queryable SQL practice environment for senior analytics engineering interviews.

## How it works

1. Pick a question from `questions/`
2. Run `python data/bootstrap.py` (builds per-question DBs and refreshes `data/workspace_verify.duckdb`)
3. Query via **`data/workspace_verify.duckdb`**: each question is a schema (`q001`, `q002`, …). Use **`scratchpad.sql`** (shared template) — attach once, then switch with `USE workspace_db.q00N;` For private notes, use **`personal_scratch.sql`** (gitignored).
4. Review `solutions/` when ready

## Setup

Python 3.9+:

```bash
pip install -r requirements.txt
```

## Data

`*.duckdb` files are gitignored. One command runs every `data/generators/generate_qNNN.py` and merges available `qNNN.duckdb` files into a snapshot:

```bash
python data/bootstrap.py
```

- **`data/workspace_build.duckdb`** — temporary merge output (safe while `workspace.duckdb` may be locked in the IDE)
- **`data/workspace_verify.duckdb`** — copy used for **scratchpad + DuckDB Explorer default** (read-only in settings when possible)
- **`data/qNNN.duckdb`** — per-question sources; if one is open in Cursor, bootstrap may skip merging that question until you detach it

**Adding a question:** `questions/…`, `data/generators/generate_qNNN.py` → `data/qNNN.duckdb`, `solutions/…`. Re-run bootstrap.

**Build task:** **Terminal → Run Build Task** (`Ctrl+Shift+B`) runs `python data/bootstrap.py`.

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/q002_monthly_revenue_trends.sql --schema q002
```

### Layout

| Path | Role |
|------|------|
| `scratchpad.sql` | Session template (attach + question switch + sanity checks) |
| `data/generators/` | Dataset scripts |
| `data/qNNN.duckdb` | Per-question DB |
| `data/workspace_verify.duckdb` | Merged snapshot for practice |
| `data/verify_solution_sql.py` | Non-interactive SQL check |

## Questions

| # | Topic | Concepts tested |
|---|-------|-----------------|
| [Q001](questions/q001_cohort_retention.md) | Cohort Retention | windows, dates, cohorts, ratios |
| [Q002](questions/q002_monthly_revenue_trends.md) | Monthly Revenue Trends | aggregation, rolling average, ranking |

## Philosophy

Questions mirror senior AE interviews: ambiguous specs, business nuance, multiple defensible SQL shapes.

## Provenance

**Tooling and scaffolding** (bootstrap, workspace snapshots, VS Code/Cursor config, generators, many solutions, and docs) were produced primarily with **Cursor’s Agent** (automated coding assistant in this repo’s chat sessions). Cursor routes requests to **vendor-managed models**; there is **no durable, public per-commit model ID** exposed in the UI, so this README does not list specific model names.

**You should review** generated SQL and Python like any other PR. Interview prompts are meant for practice, not as authoritative business definitions.
