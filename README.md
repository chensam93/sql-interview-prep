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
3. Query via **`data/duckdb/workspace_verify.duckdb`**: each question is a schema (`q001`, …). Use **`scratchpad.sql`** (shared template) — attach once, then switch with `USE workspace_db.q00N;` For private notes, use **`personal_scratch.sql`** (gitignored).
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

## Data

`*.duckdb` files are gitignored. One command runs every `data/generators/generate_qNNN.py` and merges question DBs into a single practice snapshot:

```bash
python data/bootstrap.py
```

### What the DuckDB files are

| File | Role |
|------|------|
| `data/duckdb/q001.duckdb`, … | **Source** DB for each question (what generators build). Tables live in schema `main`. |
| `data/duckdb/workspace_build.duckdb` | **Temporary** merge: copies each `qNNN` into its own schema (`q001`, …) then feeds the verify file. |
| `data/duckdb/workspace_verify.duckdb` | **What you query in practice** — one file, switch schema to change question. Safe to open while per-question files may be locked. |

If a per-question file is open in Cursor, bootstrap may skip merging that question until you detach it. Bootstrap still looks for **legacy** `data/qNNN.duckdb` if the new path is missing (one-time migration).

**Adding a question:** `questions/…`, `data/generators/generate_qNNN.py` → `data/duckdb/qNNN.duckdb`, `solutions/…`. Re-run bootstrap.

**Build task:** **Terminal → Run Build Task** (`Ctrl+Shift+B`) runs `python data/bootstrap.py`.

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/<question_solution>.sql --schema q00N
```

Examples:

```bash
python data/verify_solution_sql.py --sql solutions/q001_monthly_revenue_trends.sql --schema q001
```

### Layout

| Path | Role |
|------|------|
| `scratchpad.sql` | Session template (attach + question switch + sanity checks) |
| `data/generators/` | Dataset scripts |
| `data/duckdb/` | All `.duckdb` artifacts (per-question + workspace snapshots) |
| `data/verify_solution_sql.py` | Non-interactive SQL check |
| `progress/` | Personal progress tracking notes (public, sidecar) |

## Questions

| # | Topic | Concepts tested |
|---|-------|-----------------|
| [Q001](questions/q001_monthly_revenue_trends.md) | Monthly Revenue Trends | aggregation, rolling average, ranking |


