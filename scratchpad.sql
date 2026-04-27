-- DuckDB scratchpad
-- Keep memory.main active so workspace_db can always be detached/reattached if needed.
use memory.main;
detach database if exists workspace_db;
attach 'data/duckdb/workspace_build.duckdb' as workspace_db;

-- Switch question by editing the schema in the line below.
use workspace_db.q009_lower;

select current_database(), current_schema();

select table_name
from information_schema.tables
where table_schema = current_schema()
order by table_name;

-- Start your answer below
-- SELECT ...

