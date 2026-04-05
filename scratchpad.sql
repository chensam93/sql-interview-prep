-- Session bootstrap (run once in a fresh SQL tab/session).
-- This makes scratchpad self-contained even if DuckDB Explorer is on a different DB.
ATTACH 'data/duckdb/workspace_verify.duckdb' AS workspace_db;

-- Quick sanity checks
-- You can only set one default schema per session (USE). To see every question
-- schema after ATTACH, run the block below, then set USE to one of those names.
--
-- SELECT schema_name
-- FROM information_schema.schemata
-- WHERE catalog_name = 'workspace_db'
--   AND schema_name NOT IN ('information_schema', 'pg_catalog', 'main')
-- ORDER BY schema_name;
--
-- Switch question: edit the single USE line (or skip USE and qualify tables as
-- workspace_db.<schema>.<table>).
USE workspace_db.q002_core;

SELECT current_database(), current_schema();
SHOW TABLES;

-- Start your answer below
-- SELECT ...
