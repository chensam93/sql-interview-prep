# SQL Interview Prep

Much of this repository was built with coding-agent assistance (for example Cursor). It is a personal practice scaffold, not production software—review SQL, Python, and data logic before relying on it.

**What you get:** Interview-style prompts with **real rows in DuckDB**, so you run SQL and inspect results instead of guessing on paper.

**How to use it:** Read a prompt in `questions/` → install deps and run `bootstrap` once per refresh → open the workspace database in `scratchpad.sql`, attach the schema for that question (`use workspace_db.<schema_id>;`) → write and run your query. Peek at `solutions/` or the verify command below when you want a reference. If you use **Cursor or a similar agent**, you can iterate on prompts and regenerate data without leaving the repo.

## Stack

- **Runtime:** Python 3.9+
- **Data:** DuckDB (local `.duckdb` workspaces under `data/duckdb/`, built by `data/bootstrap.py`)
- **Authoring:** Markdown prompts, SQL solutions, Python data generators (`data/generators/`)
- **Editor (optional):** VS Code or Cursor — `.vscode/` wires DuckDB Explorer and a bootstrap build task

## Quickstart

```bash
pip install -r requirements.txt
python data/bootstrap.py
```

That installs DuckDB for Python, runs every question generator, and refreshes the merged workspace DB.

In your SQL client, open `data/duckdb/workspace_build.duckdb` (or `workspace_build_pending.duckdb` if the main file is locked on Windows — common when it is already attached). In `scratchpad.sql` (or equivalent), attach a question schema, for example:

```sql
use workspace_db.q003_core;
```

**VS Code / Cursor:** Explorer target and build task live in `.vscode/settings.json` and `.vscode/tasks.json` (`Ctrl+Shift+B` runs bootstrap).

Optional — validate a reference solution against the built data:

```bash
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
```

**Development model / snapshot:** Automation skews AI-assisted; question intent skews human-led. README snapshot: 2026-04-27.
