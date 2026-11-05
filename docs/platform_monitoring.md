
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

## Extended Platform Observability

### 1. Monitoring Snapshot

The `platform_monitoring_history` Delta table stores timestamped platform metrics.

Monitored components:
- Bronze record count
- Silver record count
- Incremental target record count
- Gold analytics table record counts
- Bronze-to-Silver reconciliation
- Silver-to-Incremental reconciliation

### 2. Delta Lake Transaction Monitoring

The observability notebook inspects Delta transaction history using DESCRIBE HISTORY.

Captured metrics include:
- Table version
- Operation type
- Execution timestamp
- MERGE execution time
- Inserted and updated records
- Output records
- Files added

### 3. Data Quality Monitoring

Historical data quality runs are grouped by run ID.

Metrics include:
- Total checks
- Passed checks
- Failed checks
- Overall run status
- Execution timestamps

### 4. Incremental Processing Monitoring

Incremental processing audit history captures:
- Source records
- Inserted records
- Updated records
- Unchanged records
- Reconciliation delta
- Processing status

### 5. Alert Evaluation

Rule-based monitoring evaluates:
- Empty pipeline tables
- Bronze-to-Silver record mismatches
- Silver-to-Incremental record mismatches
- Data quality failures
- Incremental processing failures
- Incremental reconciliation mismatches

Alert evaluations are retained in:
`workspace.video_game_sales.platform_alert_history`

Healthy evaluations are recorded as `NO_ALERTS`.

### 6. Historical Metrics

Monitoring snapshots are retained in:
`workspace.video_game_sales.platform_monitoring_history`

The notebook includes Plotly visualizations for:
- Pipeline record-count trends
- Gold analytics table volumes
- Data quality history
- Incremental processing metrics
- Delta MERGE execution times
- Alert evaluation history

### 7. Current Implementation Scope and Limitations

This project demonstrates notebook-driven, read-only platform monitoring and Delta-based metric persistence.

The current implementation does not include:
- Automated scheduled monitoring jobs
- Email, Slack, or PagerDuty notifications
- Databricks compute utilization monitoring
- Production infrastructure cost monitoring
- Enterprise workspace-level alerting

Historical trend analysis becomes meaningful as additional monitoring snapshots accumulate.
