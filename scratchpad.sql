-- Session bootstrap (run once in a fresh SQL tab/session).
-- We attach workspace_build because it is refreshed directly by bootstrap.
attach if not exists 'data/duckdb/workspace_build.duckdb' as workspace_db;

-- If this tab already attached workspace_db to an older file, run this reset block:
-- use memory.main;
-- detach workspace_db;
-- attach 'data/duckdb/workspace_build.duckdb' as workspace_db;

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
USE workspace_db.q001_lower;

SELECT current_database(), current_schema();
SHOW TABLES;

-- Start your answer below
-- SELECT ...