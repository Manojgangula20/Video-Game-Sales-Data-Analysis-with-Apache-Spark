
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_record_fingerprint(
    df: DataFrame,
    columns: list[str]
) -> DataFrame:
    """Add a deterministic SHA-256 fingerprint."""

    return df.withColumn(
        "record_hash",
        F.sha2(
            F.to_json(
                F.struct(*[F.col(c) for c in columns])
            ),
            256
        )
    )
