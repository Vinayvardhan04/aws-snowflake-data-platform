# AWS storage template

This Terraform configuration creates **two S3 buckets only**: bronze and silver. It enables public access blocks, AES-256 server-side encryption, and versioning. It does not create ingestion compute, Airflow, Glue, IAM roles, or Snowflake integrations.

Run `terraform init` and `terraform plan` after configuring your AWS credentials. Review estimated charges and resource names before `terraform apply`. Use a secured remote state backend for shared deployments. No deployment is claimed in this portfolio.
