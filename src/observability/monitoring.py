
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def collect_layer_metrics(
    spark,
    schema: str,
    layer_tables: dict
) -> list:
    """Collect record counts and availability status for pipeline tables."""

    metrics = []

    for layer, table in layer_tables.items():
        count = spark.table(f"{schema}.{table}").count()

        metrics.append((
            layer,
            int(count),
            "AVAILABLE" if count > 0 else "EMPTY"
        ))

    return metrics


def build_reconciliation_metric(
    metric_name: str,
    source_count: int,
    target_count: int
) -> tuple:
    """Compare source and target record counts."""

    difference = int(target_count - source_count)

    return (
        metric_name,
        difference,
        "PASS" if difference == 0 else "CHECK"
    )


def get_latest_dq_metrics(
    dq_audit: DataFrame
) -> dict:
    """Evaluate the latest data quality audit run."""

    latest_run = (
        dq_audit
        .orderBy(F.col("execution_timestamp").desc())
        .select("run_id")
        .first()
    )

    if latest_run is None:
        return {
            "run_id": None,
            "total_checks": 0,
            "failed_checks": 0
        }

    run_id = latest_run["run_id"]

    latest_dq = dq_audit.filter(
        F.col("run_id") == run_id
    )

    failed_checks = latest_dq.filter(
        F.upper(F.col("status")) != "PASS"
    ).count()

    return {
        "run_id": run_id,
        "total_checks": latest_dq.count(),
        "failed_checks": failed_checks
    }


def summarize_dq_history(
    dq_history: DataFrame
) -> DataFrame:
    """Summarize historical data quality runs."""

    return (
        dq_history
        .groupBy("run_id")
        .agg(
            F.count("check_name").alias("total_checks"),
            F.sum(
                F.when(
                    F.upper(F.col("status")) == "PASS", 1
                ).otherwise(0)
            ).alias("passed_checks"),
            F.sum(
                F.when(
                    F.upper(F.col("status")) != "PASS", 1
                ).otherwise(0)
            ).alias("failed_checks"),
            F.min("execution_timestamp").alias("started_at"),
            F.max("execution_timestamp").alias("last_recorded_at")
        )
        .withColumn(
            "overall_status",
            F.when(F.col("failed_checks") == 0, "PASS")
             .otherwise("CHECK")
        )
        .orderBy(F.col("last_recorded_at").desc())
    )


def summarize_incremental_history(
    incremental_history: DataFrame
) -> DataFrame:
    """Calculate incremental processing reconciliation metrics."""

    return (
        incremental_history
        .withColumn(
            "accounted_count",
            F.col("inserted_count")
            + F.col("updated_count")
            + F.col("unchanged_count")
        )
        .withColumn(
            "reconciliation_delta",
            F.col("source_count") - F.col("accounted_count")
        )
        .withColumn(
            "reconciliation_status",
            F.when(
                F.col("reconciliation_delta") == 0, "PASS"
            ).otherwise("CHECK")
        )
        .select(
            "batch_id",
            "source_count",
            "inserted_count",
            "updated_count",
            "unchanged_count",
            "accounted_count",
            "reconciliation_delta",
            "reconciliation_status",
            "status",
            "execution_timestamp"
        )
        .orderBy(F.col("execution_timestamp").desc())
    )


def build_delta_operations_monitor(
    history_frames: list
):
    """Combine Delta history and extract operation metrics."""

    if not history_frames:
        return None

    combined_history = history_frames[0]

    for frame in history_frames[1:]:
        combined_history = combined_history.unionByName(
            frame,
            allowMissingColumns=True
        )

    return (
        combined_history
        .withColumn(
            "execution_time_ms",
            F.col("operationMetrics")
            .getItem("executionTimeMs").cast("long")
        )
        .withColumn(
            "rows_inserted",
            F.col("operationMetrics")
            .getItem("numTargetRowsInserted").cast("long")
        )
        .withColumn(
            "rows_updated",
            F.col("operationMetrics")
            .getItem("numTargetRowsUpdated").cast("long")
        )
        .withColumn(
            "rows_output",
            F.col("operationMetrics")
            .getItem("numOutputRows").cast("long")
        )
        .withColumn(
            "files_added",
            F.col("operationMetrics")
            .getItem("numTargetFilesAdded").cast("long")
        )
        .select(
            "table_name",
            "version",
            "timestamp",
            "operation",
            "execution_time_ms",
            "rows_inserted",
            "rows_updated",
            "rows_output",
            "files_added"
        )
        .orderBy(
            F.col("timestamp").desc(),
            F.col("table_name")
        )
    )
