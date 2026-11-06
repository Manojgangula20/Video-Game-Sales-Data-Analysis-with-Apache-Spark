locals {
  bucket_name = "${var.name_prefix}-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.region}"

  common_tags = merge(
    {
      Component = "DataPlatform"
    },
    var.tags
  )
}

# S3 data lake bucket
resource "aws_s3_bucket" "data_lake" {
  bucket        = local.bucket_name
  force_destroy = true

  tags = merge(local.common_tags, {
    Name      = local.bucket_name
    DataLayer = "Raw"
  })
}

# Enable bucket versioning
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudWatch observability log group
resource "aws_cloudwatch_log_group" "platform" {
  name              = "/bms-databricks-platform/observability"
  retention_in_days = var.log_retention_days

  tags = merge(local.common_tags, {
    Component = "Observability"
  })
}

# Databricks Unity Catalog IAM role
resource "aws_iam_role" "databricks_s3_access" {
  name = "bms-databricks-s3-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        AWS = [
          "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL",
          "arn:aws:iam::460763906277:role/bms-databricks-s3-access"
        ]
      }
      Action = "sts:AssumeRole"
      Condition = {
        StringEquals = {
          "sts:ExternalId" = "49e904a2-05ae-4f7c-9d55-f7be44a6dfed"
        }
      }
    }]
  })

  tags = {
    Project   = "BMS-Databricks-Platform"
    ManagedBy = "Terraform"
  }
}

# Least-privilege access to the project S3 bucket
resource "aws_iam_role_policy" "databricks_s3_access" {
  name = "bms-databricks-s3-access-policy"
  role = aws_iam_role.databricks_s3_access.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.data_lake.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:AbortMultipartUpload",
          "s3:ListMultipartUploadParts"
        ]
        Resource = "${aws_s3_bucket.data_lake.arn}/*"
      },
      {
        Sid    = "ManagedFileEventsSetupStatement"
        Effect = "Allow"
        Action = [
          "s3:GetBucketNotification",
          "s3:PutBucketNotification",
          "sns:ListSubscriptionsByTopic",
          "sns:GetTopicAttributes",
          "sns:SetTopicAttributes",
          "sns:CreateTopic",
          "sns:TagResource",
          "sns:Publish",
          "sns:Subscribe",
          "sqs:CreateQueue",
          "sqs:DeleteMessage",
          "sqs:ReceiveMessage",
          "sqs:SendMessage",
          "sqs:GetQueueUrl",
          "sqs:GetQueueAttributes",
          "sqs:SetQueueAttributes",
          "sqs:TagQueue",
          "sqs:ChangeMessageVisibility",
          "sqs:PurgeQueue"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "arn:aws:sqs:*:*:csms-*",
          "arn:aws:sns:*:*:csms-*"
        ]
      },
      {
        Sid    = "ManagedFileEventsListStatement"
        Effect = "Allow"
        Action = [
          "sqs:ListQueues",
          "sqs:ListQueueTags",
          "sns:ListTopics"
        ]
        Resource = [
          "arn:aws:sqs:*:*:csms-*",
          "arn:aws:sns:*:*:csms-*"
        ]
      },
      {
        Sid    = "ManagedFileEventsTeardownStatement"
        Effect = "Allow"
        Action = [
          "sns:Unsubscribe",
          "sns:DeleteTopic",
          "sqs:DeleteQueue"
        ]
        Resource = [
          "arn:aws:sqs:*:*:csms-*",
          "arn:aws:sns:*:*:csms-*"
        ]
      }
    ]

  })
}
