
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def validate_record_count(
    source_count: int,
    target_count: int
) -> bool:
    return source_count == target_count


def count_duplicate_keys(
    df: DataFrame,
    key_column: str
) -> int:
    return (
        df.groupBy(key_column)
        .count()
        .filter(F.col("count") > 1)
        .count()
    )


def validate_unique_key(
    df: DataFrame,
    key_column: str
) -> bool:
    null_count = df.filter(
        F.col(key_column).isNull()
    ).count()

    duplicate_count = count_duplicate_keys(
        df, key_column
    )

    return null_count == 0 and duplicate_count == 0
