
# Databricks Data Platform Architecture

## 1. Project Overview

This project implements an end-to-end data engineering platform using Apache Spark, Databricks, Delta Lake and Unity Catalog.

The platform processes video game sales data through Bronze, Silver and Gold layers, supports incremental MERGE processing, and provides data quality validation and platform observability.

## 2. Architecture


flowchart TD
    A["Video Game Sales CSV"]
    B["Unity Catalog Volume"]
    C["Bronze Layer"]
    D["Silver Layer"]
    E["Data Quality Checks"]
    F["Incremental MERGE"]
    G["Gold Analytics"]

    A --> B --> C --> D
    D --> E
    D --> F
    D --> G

    E --> H["Data Quality Audit"]
    F --> I["Incremental Audit"]

    G --> J["Year"]
    G --> K["Platform"]
    G --> L["Genre"]
    G --> M["Region"]
    G --> N["Top Games"]

    subgraph OBS["Platform Observability"]
        O["Health Monitoring"]
        P["Delta History"]
        Q["Alert Evaluation"]
        R["Plotly Dashboard"]
        S["Monitoring History"]
        T["Alert History"]
        O --> S
        P --> R
        Q --> T
        S --> R
    end

    C --> O
    D --> O
    E --> O
    F --> P
    G --> O
    H --> Q
    I --> Q

    subgraph CICD["CI and Infrastructure"]
        U["GitHub Repository"]
        V["PySpark CI Tests"]
        W["Terraform CI Validation"]
        U --> V
        U --> W
    end


## 3. Data Architecture

### Bronze Layer

- Ingests source CSV records.
- Preserves original source columns.
- Captures source file path and ingestion timestamp.
- Stores data in Delta format.

### Silver Layer

- Standardizes column names and text values.
- Parses release years.
- Identifies missing or invalid years.
- Calculates regional sales totals.
- Evaluates sales reconciliation differences.

### Gold Layer

Five analytical Delta tables:

- `gold_sales_by_year`
- `gold_sales_by_platform`
- `gold_sales_by_genre`
- `gold_sales_by_region`
- `gold_top_games`

## 4. Incremental Processing

The incremental processing implementation uses Delta MERGE.

Capabilities demonstrated:

- Initial target population.
- Record fingerprinting.
- Insert and update detection.
- Idempotent reruns.
- Processing audit logging.
- Source-to-target reconciliation.

The implementation uses a full Silver snapshot as its MERGE source. It does not demonstrate CDC or watermark-based extraction.

## 5. Platform Observability

The observability notebook monitors:

- Pipeline table record counts.
- Layer reconciliation.
- Data quality audit history.
- Incremental processing audit history.
- Delta transaction history.
- MERGE execution metrics.

Persistent monitoring tables:

- `platform_monitoring_history`
- `platform_alert_history`

Interactive Plotly dashboards provide operational views.

## 6. CI/CD and Infrastructure as Code

GitHub Actions workflows:

- PySpark unit-test execution.
- Terraform formatting and validation.

Terraform configuration defines a Git-backed Databricks observability job.

The Terraform configuration has passed CI validation but has not been deployed to a live workspace.

## 7. Technology Stack

- Apache Spark / PySpark
- Databricks
- Delta Lake
- Unity Catalog
- Python
- SQL
- Plotly
- Pytest
- GitHub Actions
- Terraform
- Git / GitHub

## 8. Implementation Scope

Developed and tested using Databricks Free Edition.

The project demonstrates data engineering, incremental processing, quality validation, monitoring, and infrastructure configuration.

Production workspace administration, cloud infrastructure provisioning, automated alert notifications, and production scheduling have not been demonstrated.
