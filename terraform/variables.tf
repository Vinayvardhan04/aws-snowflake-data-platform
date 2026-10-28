variable "aws_region" {
  description = "AWS region for the data buckets"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "project" {
  description = "Short lowercase project prefix used in bucket names"
  type        = string
  default     = "vinay-events"
}
