
# Access Control and Security

## 1. Overview

This document describes the access-control considerations and security practices for the Video Game Sales Data Platform.

The platform is implemented using Databricks Free Edition, Delta Lake, Python, SQL, and Terraform.

The objective is to organize data access, protect platform resources, and establish a foundation for secure data engineering operations.

## 2. Platform Security Scope

The project uses the following platform components:

- Databricks workspace
- Unity Catalog
- Catalog and schema organization
- Delta tables
- Databricks notebooks
- Terraform infrastructure configuration
- GitHub Actions CI workflows

Access to these resources depends on the permissions supported by the configured Databricks workspace and GitHub repository.

## 3. Unity Catalog Organization

The project organizes data using the following catalog and schema:

- **Catalog:** `workspace`
- **Schema:** `video_game_sales`

The schema contains the platform's Bronze, Silver, Gold, incremental-processing, audit, and monitoring tables.

The source CSV is stored in the following Unity Catalog volume:

`workspace.video_game_sales.raw_files`

This organization provides a logical separation between source files and processed analytical data.

## 4. Data Access Principles

The following principles are recommended when managing access to the platform:

### Least Privilege

Users and service principals should receive only the permissions required to perform their responsibilities.

### Controlled Data Access

Access to source files, intermediate tables, analytical outputs, and audit records should be granted according to operational requirements.

### Separation of Responsibilities

Where supported, ingestion, transformation, analytics, and administrative responsibilities should be separated through appropriate permissions.

### Credential Protection

Credentials, access tokens, and secrets should not be committed to source control or embedded directly in notebooks.

## 5. Recommended Unity Catalog Permissions

The following permissions provide a reference model for a production deployment.

| Role | Recommended access |
|---|---|
| Platform Administrator | Workspace and catalog administration |
| Data Engineer | Required source-volume and table read/write access |
| Data Analyst | Read access to approved Gold tables |
| Auditor | Read access to audit and monitoring tables |

Actual permissions should be configured according to organizational policies and the capabilities of the deployed Databricks environment.

## 6. Terraform and Credential Management

The project includes Terraform configuration for defining a Databricks observability job.

The provider configuration uses Databricks default authentication.

Security considerations:

- Do not hard-code personal access tokens in Terraform files.
- Do not commit credentials or secrets to GitHub.
- Use environment-based or approved secret-management authentication.
- Restrict CI/CD permissions to the minimum required.
- Review Terraform plans before applying infrastructure changes.

The Terraform configuration has been validated through CI but has not been applied to a live Databricks workspace.

## 7. GitHub Actions Security

The repository includes GitHub Actions workflows for automated testing and Terraform validation.

Recommended security practices include:

- Use the minimum required workflow permissions.
- Pin third-party GitHub Actions to trusted versions or commit SHAs.
- Store sensitive credentials in GitHub Secrets or approved secret-management systems.
- Avoid exposing secrets in workflow logs.
- Review changes to workflow files before merging.

## 8. Production Security Recommendations

The following controls are recommended for a production deployment:

1. Configure role-based access control using Unity Catalog.
2. Apply least-privilege permissions to users and service principals.
3. Restrict access to raw source data where appropriate.
4. Use managed identities or approved service-principal authentication.
5. Store secrets in a centralized secret-management solution.
6. Enable audit logging and periodically review access activity.
7. Separate development, testing, and production environments.
8. Review CI/CD permissions and infrastructure changes.

These are production recommendations and should not be interpreted as controls already deployed in the current demonstration environment.

## 9. Current Implementation Status

| Security area | Project status |
|---|---|
| Unity Catalog organization | Implemented |
| Catalog and schema structure | Implemented |
| Source volume organization | Implemented |
| Terraform provider configuration | Implemented and validated |
| Terraform deployment to live workspace | Not deployed |
| Production role-based access policies | Not established by this project |
| Centralized secrets management | Not implemented |
| Production audit and identity integrations | Not implemented |

## 10. Security Considerations

The current implementation demonstrates data organization, infrastructure configuration, and security-aware development practices.

A production deployment would require additional identity integration, permission configuration, secret management, and security monitoring based on the organization's governance requirements.
