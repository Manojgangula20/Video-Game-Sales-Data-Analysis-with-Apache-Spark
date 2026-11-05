
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def transform_silver(bronze_df: DataFrame) -> DataFrame:
    """Standardize Bronze records and derive data quality fields."""

    df = bronze_df

    for column in ["Name", "Platform", "Genre", "Publisher"]:
        df = df.withColumn(column, F.trim(F.col(column)))

    df = (
        df
        .withColumnRenamed("Rank", "rank")
        .withColumnRenamed("Name", "name")
        .withColumnRenamed("Platform", "platform")
        .withColumnRenamed("Year", "year_raw")
        .withColumnRenamed("Genre", "genre")
        .withColumnRenamed("Publisher", "publisher")
        .withColumnRenamed("NA_Sales", "na_sales")
        .withColumnRenamed("EU_Sales", "eu_sales")
        .withColumnRenamed("JP_Sales", "jp_sales")
        .withColumnRenamed("Other_Sales", "other_sales")
        .withColumnRenamed("Global_Sales", "global_sales")
    )

    df = df.withColumn(
        "year",
        F.when(
            F.col("year_raw").rlike(r"^\d{4}$"),
            F.col("year_raw").cast("int")
        )
    )

    df = df.withColumn(
        "year_status",
        F.when(F.col("year").isNotNull(), "VALID")
         .otherwise("MISSING_OR_INVALID")
    )

    df = df.withColumn(
        "regional_sales_total",
        F.round(
            F.col("na_sales") +
            F.col("eu_sales") +
            F.col("jp_sales") +
            F.col("other_sales"),
            2
        )
    )

    df = df.withColumn(
        "sales_difference",
        F.round(
            F.abs(F.col("global_sales") - F.col("regional_sales_total")),
            2
        )
    )

    df = df.withColumn(
        "sales_reconciliation_status",
        F.when(F.col("sales_difference") == 0, "MATCH")
         .otherwise("DIFFERENCE_DETECTED")
    )

    return df
