
# Databricks Observability Job - Terraform

## Purpose

Manage the Databricks platform observability job using Terraform.

## Managed Resource

- Databricks single-task job using serverless compute
- GitHub-backed notebook source
- Retry configuration
- Execution timeout
- Concurrency control
- Resource tags

## Authentication

Configure these environment variables securely:

- DATABRICKS_HOST
- DATABRICKS_TOKEN

Never commit access tokens or credentials.

## Deployment

Initialize:

    terraform init

Format:

    terraform fmt -recursive

Validate:

    terraform validate

Review proposed changes:

    terraform plan

Apply only after verifying workspace permissions,
compute availability and the proposed resource changes.

## Scope

This configuration manages the observability job only.

It does not provision the Databricks workspace,
cloud infrastructure, Unity Catalog or compute resources.

The initial job has no automatic schedule.
