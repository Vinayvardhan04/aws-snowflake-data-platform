-- Run with an account role permitted to create databases and warehouses.
-- This creates a raw table for normalized records; loading from S3 requires
-- a separately configured Snowflake storage integration.
CREATE DATABASE IF NOT EXISTS DE_PLATFORM;
CREATE SCHEMA IF NOT EXISTS DE_PLATFORM.RAW;
CREATE SCHEMA IF NOT EXISTS DE_PLATFORM.ANALYTICS;

CREATE WAREHOUSE IF NOT EXISTS DE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

CREATE TABLE IF NOT EXISTS DE_PLATFORM.RAW.GITHUB_EVENTS (
  EVENT_ID VARCHAR NOT NULL,
  EVENT_TYPE VARCHAR NOT NULL,
  REPO_NAME VARCHAR NOT NULL,
  ACTOR VARCHAR NOT NULL,
  CREATED_AT TIMESTAMP_TZ NOT NULL,
  EVENT_DATE DATE NOT NULL
);

-- Snowflake does not enforce standard unique constraints on this table type.
-- Deduplicate by EVENT_ID before loading and use a MERGE for incremental loads.
