# SQL Interview Prep

Much of this repository was built with coding-agent assistance (for example Cursor). It is a personal practice scaffold, not production software—review SQL, Python, and data logic before relying on it.

**What you get:** Interview-style prompts with **real rows in DuckDB**, so you run SQL and inspect results instead of guessing on paper or having to rely on a LLM's response. I've found extra value in being able to work with a query itself and actually execute it while still having the flexibility of a LLM to generate and curate questions.

**How to use it:** Once things are setup the workflow should be simply using a scratchpad.sql (or somethign equivalent) to work on the available questions. The user should be able to easily refer to an AI of their choice to create/edit any question to their liking. Any part of the installation that is giving difficutly can likely be solved via an AI with awareness of this repository.

## Quickstart

```bash
pip install -r requirements.txt
python data/bootstrap.py
```

In `scratchpad.sql`, attach the workspace file under `data/duckdb/` (often `workspace_build.duckdb`; if it is locked on Windows, use `workspace_build_pending.duckdb` instead), then for example:

```sql
use workspace_db.q003_core;
```

**VS Code / Cursor:** DuckDB Explorer is pointed at `data/duckdb/workspace_verify.duckdb` in `.vscode/settings.json`. **Run Build Task** (`Ctrl+Shift+B`) runs bootstrap again.

Optional—check a reference solution against the built data:

```bash
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
```

**Development model / snapshot:** Automation skews AI-assisted; question intent skews human-led. README snapshot: 2026-04-27.
