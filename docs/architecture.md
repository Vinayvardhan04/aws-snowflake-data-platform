# Architecture and tradeoffs

## Local implementation

The local CLI separates raw input (bronze) from normalized records (silver) and stores unique events in SQLite. A primary key on `event_id` makes reloads idempotent. `event_date` is derived after converting timestamps to UTC, preventing cross-timezone grouping errors. Invalid records are counted and excluded; the raw input remains available for inspection.

The sample API contains only recent events and does not guarantee complete historical coverage. The CLI fetches one page of 100 public events. A production extractor would need pagination, rate-limit handling, durable cursors, retries, and backfill strategy. No production uptime or cost claims are made here.

## Cloud extension

Terraform provisions S3 buckets for bronze and silver data with encryption, versioning, and public access blocks. For an AWS deployment, a scheduler and ingestion runtime would write bronze objects; a batch transform would produce silver Parquet; a configured Snowflake storage integration would expose the silver path to Snowflake. dbt would then build tested analytics marts. These runtimes and the storage integration are intentionally **not** provisioned by the current Terraform configuration.

## Security and operations

Do not commit GitHub tokens or cloud credentials. A production deployment should use short-lived identity credentials, a Snowflake storage integration, least-privilege IAM, state locking, monitoring for failed loads and freshness, and cost budgets. Terraform state must be stored in a secured remote backend before team use.
