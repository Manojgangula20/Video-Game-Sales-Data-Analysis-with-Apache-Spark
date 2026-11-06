
from datetime import datetime

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    TimestampType,
    MapType,
)

from src.observability.monitoring import (
    collect_layer_metrics,
    build_reconciliation_metric,
    get_latest_dq_metrics,
    summarize_dq_history,
    summarize_incremental_history,
    build_delta_operations_monitor,
)


def test_collect_layer_metrics():
    class FakeTable:
        def __init__(self, count):
            self.record_count = count

        def count(self):
            return self.record_count

    class FakeSpark:
        def table(self, name):
            return FakeTable({
                "test_schema.bronze": 100,
                "test_schema.gold": 0,
            }[name])

    result = collect_layer_metrics(
        FakeSpark(),
        "test_schema",
        {
            "BRONZE": "bronze",
            "GOLD": "gold",
        },
    )

    assert result == [
        ("BRONZE", 100, "AVAILABLE"),
        ("GOLD", 0, "EMPTY"),
    ]


def test_build_reconciliation_metric():
    passed = build_reconciliation_metric(
        "BRONZE_SILVER",
        100,
        100,
    )

    failed = build_reconciliation_metric(
        "SILVER_INCREMENTAL",
        100,
        98,
    )

    assert passed == ("BRONZE_SILVER", 0, "PASS")
    assert failed == ("SILVER_INCREMENTAL", -2, "CHECK")


def test_get_latest_dq_metrics(spark):
    records = [
        ("run_old", "CHECK_A", "PASS", datetime(2026, 1, 1)),
        ("run_old", "CHECK_B", "FAIL", datetime(2026, 1, 1)),
        ("run_new", "CHECK_A", "PASS", datetime(2026, 1, 2)),
        ("run_new", "CHECK_B", "PASS", datetime(2026, 1, 2)),
    ]

    schema = [
        "run_id",
        "check_name",
        "status",
        "execution_timestamp",
    ]

    dq_df = spark.createDataFrame(records, schema)

    result = get_latest_dq_metrics(dq_df)

    assert result["run_id"] == "run_new"
    assert result["total_checks"] == 2
    assert result["failed_checks"] == 0


def test_get_latest_dq_metrics_empty(spark):
    schema = """
        run_id STRING,
        check_name STRING,
        status STRING,
        execution_timestamp TIMESTAMP
    """

    dq_df = spark.createDataFrame([], schema)

    result = get_latest_dq_metrics(dq_df)

    assert result == {
        "run_id": None,
        "total_checks": 0,
        "failed_checks": 0,
    }


def test_summarize_dq_history(spark):
    records = [
        ("run_1", "CHECK_A", "PASS", datetime(2026, 1, 1)),
        ("run_1", "CHECK_B", "FAIL", datetime(2026, 1, 1)),
        ("run_2", "CHECK_A", "PASS", datetime(2026, 1, 2)),
        ("run_2", "CHECK_B", "PASS", datetime(2026, 1, 2)),
    ]

    schema = [
        "run_id",
        "check_name",
        "status",
        "execution_timestamp",
    ]

    dq_df = spark.createDataFrame(records, schema)

    result = summarize_dq_history(dq_df)

    rows = {
        row["run_id"]: row
        for row in result.collect()
    }

    assert rows["run_1"]["total_checks"] == 2
    assert rows["run_1"]["failed_checks"] == 1
    assert rows["run_1"]["overall_status"] == "CHECK"

    assert rows["run_2"]["passed_checks"] == 2
    assert rows["run_2"]["failed_checks"] == 0
    assert rows["run_2"]["overall_status"] == "PASS"


def test_summarize_incremental_history(spark):
    records = [
        (
            "batch_1", 100, 10, 5, 85,
            "SUCCESS", datetime(2026, 1, 1)
        ),
        (
            "batch_2", 100, 10, 5, 80,
            "SUCCESS", datetime(2026, 1, 2)
        ),
    ]

    schema = [
        "batch_id",
        "source_count",
        "inserted_count",
        "updated_count",
        "unchanged_count",
        "status",
        "execution_timestamp",
    ]

    incremental_df = spark.createDataFrame(records, schema)

    result = summarize_incremental_history(incremental_df)

    rows = {
        row["batch_id"]: row
        for row in result.collect()
    }

    assert rows["batch_1"]["accounted_count"] == 100
    assert rows["batch_1"]["reconciliation_delta"] == 0
    assert rows["batch_1"]["reconciliation_status"] == "PASS"

    assert rows["batch_2"]["accounted_count"] == 95
    assert rows["batch_2"]["reconciliation_delta"] == 5
    assert rows["batch_2"]["reconciliation_status"] == "CHECK"


def test_build_delta_operations_monitor(spark):
    schema = StructType([
        StructField("table_name", StringType(), False),
        StructField("version", LongType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("operation", StringType(), False),
        StructField(
            "operationMetrics",
            MapType(StringType(), StringType()),
            True,
        ),
    ])

    records = [
        (
            "incremental_video_game_sales",
            5,
            datetime(2026, 1, 1),
            "MERGE",
            {
                "executionTimeMs": "120",
                "numTargetRowsInserted": "2",
                "numTargetRowsUpdated": "3",
                "numOutputRows": "5",
                "numTargetFilesAdded": "1",
            },
        )
    ]

    history_df = spark.createDataFrame(records, schema)

    result = build_delta_operations_monitor([history_df])

    row = result.first()

    assert row["table_name"] == "incremental_video_game_sales"
    assert row["execution_time_ms"] == 120
    assert row["rows_inserted"] == 2
    assert row["rows_updated"] == 3
    assert row["rows_output"] == 5
    assert row["files_added"] == 1


def test_build_delta_operations_monitor_empty():
    assert build_delta_operations_monitor([]) is None
