
from src.quality.checks import (
    validate_record_count,
    count_duplicate_keys,
    validate_unique_key
)


def test_record_count_validation():
    assert validate_record_count(100, 100) is True
    assert validate_record_count(100, 99) is False


def test_unique_key_validation(spark):
    unique_df = spark.createDataFrame(
        [(1, "A"), (2, "B"), (3, "C")],
        ["rank", "name"]
    )

    assert validate_unique_key(unique_df, "rank") is True


def test_duplicate_key_detection(spark):
    duplicate_df = spark.createDataFrame(
        [(1, "A"), (1, "B"), (2, "C")],
        ["rank", "name"]
    )

    assert count_duplicate_keys(duplicate_df, "rank") == 1
    assert validate_unique_key(duplicate_df, "rank") is False


def test_null_key_detection(spark):
    null_df = spark.createDataFrame(
        [(1, "A"), (None, "B")],
        ["rank", "name"]
    )

    assert validate_unique_key(null_df, "rank") is False
