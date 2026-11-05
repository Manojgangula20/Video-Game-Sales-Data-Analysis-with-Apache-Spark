
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp


def ingest_bronze(
    spark,
    source_path: str,
    target_table: str
) -> int:
    """Ingest CSV data into a managed Bronze Delta table."""

    raw_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(source_path)
    )

    bronze_df = (
        raw_df
        .select("*", col("_metadata.file_path").alias("source_file"))
        .withColumn("ingestion_timestamp", current_timestamp())
    )

    record_count = bronze_df.count()

    (
        bronze_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )

    return record_count
