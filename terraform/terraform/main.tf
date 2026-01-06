terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ---------------------------
# S3 Buckets – Data Lake
# ---------------------------

resource "aws_s3_bucket" "bronze" {
  bucket = "de-bronze-${var.environment}"
}

resource "aws_s3_bucket" "silver" {
  bucket = "de-silver-${var.environment}"
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "de-artifacts-${var.environment}"
}
