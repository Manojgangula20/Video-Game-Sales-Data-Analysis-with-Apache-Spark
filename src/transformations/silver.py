from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def transform_silver(bronze_df: DataFrame) -> DataFrame:
    """
    Transform Bronze data into the standardized Silver layer.

    Operations:
    - Trim text columns
    - Standardize column names
    - Cast sales columns to double
    - Preserve raw year values
    - Parse valid years
    - Add year quality status
    - Calculate regional sales totals
    - Reconcile regional and global sales
    """

    df = bronze_df

    # 1. Trim text columns
    for column in ["Name", "Platform", "Genre", "Publisher"]:
        df = df.withColumn(
            column,
            F.trim(F.col(column))
        )

    # 2. Standardize column names
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

    # 3. Cast sales columns to double
    sales_columns = [
        "na_sales",
        "eu_sales",
        "jp_sales",
        "other_sales",
        "global_sales"
    ]

    for column in sales_columns:
        df = df.withColumn(
            column,
            F.col(column).cast("double")
        )

    # 4. Convert valid year values
    df = df.withColumn(
        "year",
        F.when(
            F.col("year_raw").rlike(r"^\d{4}$"),
            F.col("year_raw").cast("int")
        )
    )

    # 5. Add year quality status
    df = df.withColumn(
        "year_status",
        F.when(
            F.col("year").isNotNull(),
            F.lit("VALID")
        ).otherwise(
            F.lit("MISSING_OR_INVALID")
        )
    )

    # 6. Calculate regional sales total
    df = df.withColumn(
        "regional_sales_total",
        F.round(
            F.coalesce(F.col("na_sales"), F.lit(0.0)) +
            F.coalesce(F.col("eu_sales"), F.lit(0.0)) +
            F.coalesce(F.col("jp_sales"), F.lit(0.0)) +
            F.coalesce(F.col("other_sales"), F.lit(0.0)),
            2
        )
    )

    # 7. Calculate sales reconciliation difference
    df = df.withColumn(
        "sales_difference",
        F.round(
            F.abs(
                F.col("global_sales") -
                F.col("regional_sales_total")
            ),
            2
        )
    )

    # 8. Add reconciliation status
    df = df.withColumn(
        "sales_reconciliation_status",
        F.when(
            F.col("sales_difference") == 0,
            F.lit("MATCH")
        ).otherwise(
            F.lit("DIFFERENCE_DETECTED")
        )
    )

    return df