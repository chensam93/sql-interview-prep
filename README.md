# SQL Interview Prep

A live, queryable SQL practice environment for analytics engineering interviews (personal project).
I wanted to practice my SQL for analytic engineer technical interviews but I didn't want to rely on Leetcode or similar websites. I just wanted to use Cursor and adjust the questions/parameters myself. It's easy to curate questions oneself via an LLM but I wanted data to actually query, not simply respond with SQL that I can't manually verify.

## Practice-Only Disclaimer
This repo is my SQL interview practice scaffolding. It is not intended as a public package, production system, or reference implementation for others to consume.

Expect incomplete/iterating code; review any SQL/Python before relying on it.

## Note on AI assistance
Vast majority of code was produced with **Cursor’s Agent**. My best-effort estimate:

- Repo wiring & “how to run” glue (VS Code/Cursor config, `data/bootstrap.py`, per-question generators, verify script, scratchpad wiring): ~70–90% AI-assisted.
- Interview content (the question markdown prompts + question-specific solution SQL in `solutions/`): ~20–40% AI-assisted (mostly for SQL shape/debugging), with the core modeling/intent mostly coming from me.

This is very much **vibe-coded**—treat it as a practice scaffold/draft, not a polished library. Review any generated code before relying on it.

## How it works

1. Pick a question from `questions/`
2. Run `python data/bootstrap.py` (writes per-question DBs under `data/duckdb/` and refreshes `data/duckdb/workspace_verify.duckdb`)
3. Query via **`data/duckdb/workspace_build.duckdb`** in `scratchpad.sql`: each question is a schema (`q001_lower`, `q001_core`, `q001_higher`, …). Attach once, then switch with `USE workspace_db.<schema_id>;` For private notes, use **`personal_scratch.sql`** (gitignored).
4. Review `solutions/` when ready

## Config notes (requirements + editor)
- Requirements: `python 3.9+`, and `pip install -r requirements.txt` (only `duckdb`).
- Editor integration: `.vscode/settings.json` points DuckDB Explorer at `data/duckdb/workspace_verify.duckdb` and opens it read-only.
- Build task: `.vscode/tasks.json` defines `SQL Prep: Build all DuckDB data` (runs `python data/bootstrap.py`).
- Windows: DuckDB files can be locked; if you have a `data/duckdb/qNNN.duckdb` open in Cursor, bootstrap may skip that question until you detach it (rerun bootstrap after closing).

## Setup

Python 3.9+:

```bash
pip install -r requirements.txt
```

## Secret scanning

- local pre-commit hook lives at `.githooks/pre-commit`
- CI scan runs in `.github/workflows/secret-scan.yml`
- gitleaks config lives at `.gitleaks.toml`

One-time local setup in this repo:

```bash
git config core.hooksPath .githooks
```

Optional (better local detection): install `gitleaks` so the hook runs `gitleaks protect --staged` instead of fallback regex scanning.

## Data

`*.duckdb` files are gitignored. One command runs every `data/generators/generate_q*.py` and merges question DBs into a single practice snapshot:

```bash
python data/bootstrap.py
```

### What the DuckDB files are

| File | Role |
|------|------|
| `data/duckdb/q001_core.duckdb`, `q001_lower.duckdb`, … | **Source** DB for each question (what generators build). Tables live in schema `main`. |
| `data/duckdb/workspace_build.duckdb` | **What scratchpad queries in practice** — merged schemas (`q001_core`, `q001_lower`, …) refreshed directly by bootstrap. |
| `data/duckdb/workspace_verify.duckdb` | Read-only snapshot copy for editor integrations that expect a stable file path. |

`scratchpad.sql` now runs this reset automatically at the top of each run:

```sql
use memory.main;
detach database if exists workspace_db;
attach 'data/duckdb/workspace_build.duckdb' as workspace_db;
```

When `workspace_build.duckdb` is locked (common on Windows with an attached SQL tab), bootstrap now builds to a fallback file and writes the active path to:

`data/duckdb/workspace_last_build.txt`

Bootstrap also auto-updates `scratchpad.sql` to attach whichever workspace file was built in that run (primary or fallback), so you can rerun scratchpad without manual copy/paste.

If a per-question file is open in Cursor, bootstrap may skip merging that question until you detach it. Bootstrap still looks for **legacy** `data/qNNN.duckdb` if the new path is missing (one-time migration).

**Adding a question:** add files under bucketed folders in `questions/` and `solutions/`, plus `data/generators/generate_q...py` that writes `data/duckdb/<schema_id>.duckdb`. Re-run bootstrap.

**Build task:** **Terminal → Run Build Task** (`Ctrl+Shift+B`) runs `python data/bootstrap.py`.

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/<bucket>/<question_solution>.sql --schema <schema_id>
```

Examples:

```bash
python data/verify_solution_sql.py --sql solutions/lower/q001_conversion_funnel_basics.sql --schema q001_lower
python data/verify_solution_sql.py --sql solutions/lower/q002_resolution_rate_by_channel.sql --schema q002_lower
python data/verify_solution_sql.py --sql solutions/lower/q003_priority_mix_by_channel.sql --schema q003_lower
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
python data/verify_solution_sql.py --sql solutions/core/q002_channel_customer_mix.sql --schema q002_core
python data/verify_solution_sql.py --sql solutions/core/q003_monthly_net_after_returns.sql --schema q003_core
python data/verify_solution_sql.py --sql solutions/higher/q001_subscription_mrr_movements.sql --schema q001_higher
```

### Layout

| Path | Role |
|------|------|
| `scratchpad.sql` | Session template (attach + question switch + sanity checks) |
| `data/generators/` | Dataset scripts |
| `data/duckdb/` | All `.duckdb` artifacts (per-question + workspace snapshots) |
| `data/verify_solution_sql.py` | Non-interactive SQL check |

## Questions

| # | Difficulty bucket | Topic | Concepts tested |
|---|-------------------|-------|-----------------|
| [Q001](questions/lower/q001_conversion_funnel_basics.md) | lower | Weekly Ticket Resolution Basics | left join filtering, count distinct, date bucketing, case statements |
| [Q002](questions/lower/q002_resolution_rate_by_channel.md) | lower | 7-Day Resolution Rate by Channel | left join, case statements, grouped aggregation |
| [Q003](questions/lower/q003_priority_mix_by_channel.md) | lower | Priority Mix by Channel | conditional aggregation, grouped counts, case statements |
| [Q001](questions/core/q001_monthly_revenue_trends.md) | core (mid + senior blend) | Monthly Revenue Trends | aggregation, rolling average, ranking |
| [Q002](questions/core/q002_channel_customer_mix.md) | core (mid + senior blend) | Channel Revenue Mix (New vs Returning) | ctes, window functions, conditional aggregation, ranking |
| [Q003](questions/core/q003_monthly_net_after_returns.md) | core (mid + senior blend) | Monthly gross vs refunds | ctes, joins, aggregation, coalesce, null-safe ratios |
| [Q001](questions/higher/q001_subscription_mrr_movements.md) | higher | Subscription MRR Movements | ctes, window functions, lifecycle classification |


