-- Snowflake setup for AWS Snowflake Data Platform
-- Documented for reproducibility (no execution required)

-- Database and schemas
CREATE DATABASE DE_PLATFORM;

CREATE SCHEMA DE_PLATFORM.RAW;
CREATE SCHEMA DE_PLATFORM.ANALYTICS;

-- Warehouse
CREATE WAREHOUSE DE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- External stage (S3 Silver layer)
CREATE STAGE github_silver_stage
URL='s3://de-silver-dev/github_events/'
FILE_FORMAT=(TYPE=PARQUET);

-- Raw table
CREATE TABLE RAW.GITHUB_EVENTS (
  event_id STRING,
  event_type STRING,
  repo_name STRING,
  actor STRING,
  created_at TIMESTAMP,
  event_date DATE
);
