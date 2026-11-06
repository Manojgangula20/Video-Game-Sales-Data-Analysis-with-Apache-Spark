
# AWS Data Platform Infrastructure

Terraform-managed AWS infrastructure for the Databricks Video Game Sales Lakehouse portfolio project.

## Architecture and Resources

This module provisions:

- S3 data lake bucket
- S3 bucket versioning
- AES-256 server-side encryption
- S3 public access protection
- CloudWatch observability log group
- IAM role for Databricks Unity Catalog access
- IAM inline policy for S3 data access and Databricks File Events operations
- Resource tagging

## Region

Default AWS region: `ap-south-1` (Mumbai).

## Authentication

Uses the AWS provider's standard credential chain.

Configure credentials through environment variables or an approved AWS CLI profile.

Never commit AWS credentials, secrets, Terraform state files, or generated plans.

## Deployment

Run these commands from this directory:

Initialize:

    terraform init

Format:

    terraform fmt -recursive

Validate:

    terraform validate

Review the proposed changes:

    terraform plan

Deploy only after reviewing and approving the plan:

    terraform apply

Inspect outputs:

    terraform output

## Databricks Integration

The module provisions an AWS IAM role trusted by Databricks Unity Catalog.

The trust configuration supports:

- Databricks Unity Catalog role assumption
- External ID validation
- IAM role self-assumption

The resulting role is used by a Databricks Unity Catalog storage credential and external location.

The Databricks workspace itself is not provisioned by this module. Storage credentials, external locations, and volumes are configured in Databricks.

## Security Controls

- S3 server-side encryption using AES-256
- S3 versioning enabled
- All four S3 public access block settings enabled
- IAM permissions scoped to project resources and required Databricks File Events operations
- CloudWatch log retention configured for 14 days
- Terraform-managed resource tagging

## Cleanup

After collecting project evidence, review the Terraform state and deployment plan before destroying resources.

    terraform plan -destroy

If the plan is correct and the project resources are ready for removal:

    terraform destroy

The S3 bucket currently uses `force_destroy = true`. This allows Terraform to remove objects when destroying the bucket. Confirm that no required data remains before cleanup.

Verify AWS resources manually after destruction.

Retain Terraform source files and the state backup until cleanup has been verified.

## Scope and Limitations

This module provisions the AWS infrastructure and IAM trust configuration required for the project.

It does not provision:

- A Databricks workspace
- Databricks compute infrastructure
- Databricks Unity Catalog objects
- Databricks notebooks or jobs

These are managed separately through Databricks.
