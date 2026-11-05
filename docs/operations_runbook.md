
# Operations Runbook

## 1. Overview

This runbook describes how to execute, validate, and troubleshoot the Video Game Sales Data Platform.

The platform uses Databricks notebooks and Delta tables to implement a Bronze → Silver → Gold data processing pipeline.

## 2. Environment

- **Platform:** Databricks Free Edition
- **Compute:** Serverless
- **Catalog:** `workspace`
- **Schema:** `video_game_sales`
- **Source file:** `video_game_sales.csv`
- **Source volume:** `workspace.video_game_sales.raw_files`

## 3. Pipeline Execution

Execute the notebooks in the following order:

1. `00_environment_validation`
2. `01_bronze_ingestion`
3. `02_silver_transformation`
4. `03_data_quality`
5. `04_gold_analytics`
6. `05_incremental_processing`
7. `06_platform_observability`

The environment validation notebook should be executed first to confirm that the source file and required catalog objects are accessible.

## 4. Data Validation

Verify the Bronze and Silver table counts:

```sql
SELECT COUNT(*)
FROM workspace.video_game_sales.bronze_video_game_sales;

SELECT COUNT(*)
FROM workspace.video_game_sales.silver_video_game_sales;
```

The baseline dataset contains 16,598 records.

Inspect data quality results:

```sql
SELECT *
FROM workspace.video_game_sales.data_quality_audit
ORDER BY execution_timestamp DESC;
```

Review failed checks:

```sql
SELECT *
FROM workspace.video_game_sales.data_quality_audit
WHERE status <> 'PASS'
ORDER BY execution_timestamp DESC;
```

## 5. Gold Analytics Validation

Verify the analytical output tables:

```sql
SELECT COUNT(*) FROM workspace.video_game_sales.gold_sales_by_year;

SELECT COUNT(*) FROM workspace.video_game_sales.gold_sales_by_platform;

SELECT COUNT(*) FROM workspace.video_game_sales.gold_sales_by_genre;

SELECT COUNT(*) FROM workspace.video_game_sales.gold_sales_by_region;

SELECT COUNT(*) FROM workspace.video_game_sales.gold_top_games;
```

Compare the results against the expected baseline:

- Yearly sales: 40 records
- Platform sales: 31 records
- Genre sales: 12 records
- Regional sales: 4 records
- Top games: 10 records

## 6. Incremental Processing

The incremental processing notebook uses Delta MERGE operations and SHA-256 fingerprints to identify inserted, updated, and unchanged records.

Inspect the incremental processing audit:

```sql
SELECT *
FROM workspace.video_game_sales.incremental_processing_audit
ORDER BY execution_timestamp DESC;
```

Validate target uniqueness:

```sql
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT rank) AS distinct_ranks
FROM workspace.video_game_sales.incremental_video_game_sales;
```

The current implementation processes a full Silver snapshot. It is not a CDC or watermark-based ingestion implementation.

## 7. Observability

Execute `06_platform_observability` to inspect:

- Delta table history
- Pipeline monitoring history
- Alert history
- Data quality status
- Platform-level operational metrics

The monitoring implementation is notebook-driven and does not currently represent a continuously running monitoring service.

## 8. Troubleshooting

### Source file not found

Verify that the source CSV exists in:

`/Volumes/workspace/video_game_sales/raw_files/video_game_sales.csv`

### Table or schema not found

Confirm the active catalog and schema:

```sql
SELECT CURRENT_CATALOG(), CURRENT_SCHEMA();
```

Verify that the required schema exists before executing pipeline notebooks.

### Data quality checks fail

Inspect `data_quality_audit` to identify the failed check.

Review the corresponding Silver transformation and source records before rerunning downstream notebooks.

### Incremental processing produces unexpected results

Inspect the incremental audit table and compare the target table against the current Silver snapshot.

Do not reset or overwrite the incremental target without first reviewing the existing data and audit history.

## 9. Operational Limitations

- The pipeline is executed through Databricks notebooks.
- Production scheduling has not been deployed.
- Terraform configuration defines a Databricks job but has not been applied to a live workspace.
- Incremental processing uses a full Silver snapshot rather than CDC.
- Monitoring and alerting are implemented within the notebook workflow.
