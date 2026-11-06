provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "BMS-Databricks-Platform"
      Environment = "Portfolio"
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
