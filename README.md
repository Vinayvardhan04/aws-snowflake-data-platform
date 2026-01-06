# AWS Snowflake Data Platform

## Overview
This project implements a **production-grade end-to-end data engineering platform**
using AWS and Snowflake. It demonstrates real-world patterns for data ingestion,
processing, orchestration, infrastructure automation, and analytics.

## Architecture
**Ingestion**
- GitHub Public Events API
- AWS Lambda for API ingestion
- Raw data stored in Amazon S3 (Bronze layer)

**Processing**
- AWS Glue (PySpark) for batch transformations
- Cleaned and deduplicated data stored in S3 (Silver layer)

**Analytics**
- Snowflake as the cloud data warehouse
- dbt for transformations and analytics-ready models (Gold layer)

**Orchestration & DevOps**
- Apache Airflow for workflow orchestration
- Terraform for Infrastructure as Code (IaC)
- GitHub Actions for CI/CD
- IAM with least-privilege access

## Tech Stack
AWS (S3, Lambda, Glue, IAM), Snowflake, PySpark, Airflow, dbt, Terraform, GitHub Actions

## Data Lake Design
- **Bronze**: Raw API data (JSON)
- **Silver**: Cleaned & transformed data (Parquet)
- **Gold**: Analytics-ready tables in Snowflake

## Deployment (Optional)
```bash
cd terraform
terraform init
terraform plan
terraform apply
