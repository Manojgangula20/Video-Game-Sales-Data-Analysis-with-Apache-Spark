
# Databricks Platform Monitoring

## 1. Overview

This document describes the monitoring and operational observability approach for the Video Game Sales Data Platform.

The platform uses Databricks, Apache Spark, Delta Lake and Unity Catalog.

## 2. Pipeline Monitoring

| Pipeline | Monitoring focus |
|---|---|
| Bronze | Source ingestion, record counts, ingestion timestamps |
| Silver | Transformation failures, invalid records, reconciliation |
| Data Quality | Validation results, failed checks, audit history |
| Gold | Aggregation counts and analytical table availability |
| Incremental | Insert, update, unchanged counts and MERGE results |

## 3. Delta Lake Monitoring

Monitor:
- Table history and write operations
- Record counts and schema changes
- Failed or repeated operations
- Data consistency after MERGE operations

Useful command:

```sql
DESCRIBE HISTORY workspace.video_game_sales.incremental_video_game_sales;
```

## 4. Unity Catalog Monitoring

Inspect:
- Catalog and schema availability
- Table ownership
- Object permissions
- Volume accessibility
- Unauthorized access or permission failures

## 5. Operational Metrics

| Metric | Purpose |
|---|---|
| Source record count | Verify ingestion completeness |
| Silver record count | Verify transformation reconciliation |
| Invalid year count | Track data quality |
| Inserted records | Track incremental ingestion |
| Updated records | Track changed records |
| Unchanged records | Measure idempotency |
| Pipeline execution status | Identify failures |

## 6. Troubleshooting

| Issue | Investigation |
|---|---|
| Ingestion failure | Verify source path and file availability |
| Permission denied | Inspect Unity Catalog privileges |
| MERGE failure | Validate source keys and target schema |
| Record count mismatch | Reconcile Bronze, Silver and Gold |
| Slow execution | Inspect query plans and execution metrics |

## 7. Environment Limitations

This project is developed using Databricks Free Edition.

Production workspace administration, configurable compute policies, enterprise alerting and cloud infrastructure provisioning are not claimed as completed capabilities.

These are documented as future production deployment considerations.
