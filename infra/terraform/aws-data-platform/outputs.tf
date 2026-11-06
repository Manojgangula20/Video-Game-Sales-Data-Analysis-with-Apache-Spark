output "aws_account_id" {
  description = "AWS account hosting the project infrastructure."
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS deployment region."
  value       = data.aws_region.current.region
}

output "s3_bucket_name" {
  description = "Project data lake bucket name."
  value       = aws_s3_bucket.data_lake.id
}

output "s3_bucket_arn" {
  description = "Project data lake bucket ARN."
  value       = aws_s3_bucket.data_lake.arn
}

output "cloudwatch_log_group_name" {
  description = "Platform observability log group."
  value       = aws_cloudwatch_log_group.platform.name
}

output "cloudwatch_log_group_arn" {
  description = "Platform observability log group ARN."
  value       = aws_cloudwatch_log_group.platform.arn
}

output "databricks_s3_access_role_arn" {
  description = "IAM role ARN for Databricks Unity Catalog S3 access."
  value       = aws_iam_role.databricks_s3_access.arn
}
