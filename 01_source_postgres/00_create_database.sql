-- Run against the default "postgres" database:
--   psql -h localhost -U meridian -d postgres -f 00_create_database.sql
-- CREATE DATABASE cannot run inside a transaction block, so it lives in its own file.

SELECT 'CREATE DATABASE meridian_core'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'meridian_core')\gexec

\connect meridian_core

-- pgcrypto gives gen_random_uuid(); it is used for reference numbers.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

COMMENT ON DATABASE meridian_core IS
  'Meridian Bank core banking OLTP system (teaching replica). Source for the Snowflake warehouse.';
