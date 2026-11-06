
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def sales_by_year(df: DataFrame) -> DataFrame:
    """Aggregate game counts and global sales by release year."""

    return (
        df
        .withColumn(
            "release_year",
            F.coalesce(F.col("year").cast("string"), F.lit("UNKNOWN"))
        )
        .groupBy("release_year")
        .agg(
            F.count("*").alias("game_count"),
            F.round(F.sum("global_sales"), 2).alias("global_sales")
        )
    )


def sales_by_platform(df: DataFrame) -> DataFrame:
    """Aggregate game counts and global sales by platform."""

    return (
        df
        .groupBy("platform")
        .agg(
            F.count("*").alias("game_count"),
            F.round(F.sum("global_sales"), 2).alias("global_sales")
        )
        .orderBy(F.desc("global_sales"))
    )


def sales_by_genre(df: DataFrame) -> DataFrame:
    """Aggregate game counts and global sales by genre."""

    return (
        df
        .groupBy("genre")
        .agg(
            F.count("*").alias("game_count"),
            F.round(F.sum("global_sales"), 2).alias("global_sales")
        )
        .orderBy(F.desc("global_sales"))
    )


def regional_sales(df: DataFrame) -> DataFrame:
    """Aggregate sales across the four geographic regions."""

    region_columns = [
        ("NA", "na_sales"),
        ("EU", "eu_sales"),
        ("JP", "jp_sales"),
        ("OTHER", "other_sales")
    ]

    region_df = None

    for region_name, column_name in region_columns:
        current_region = df.agg(
            F.lit(region_name).alias("region"),
            F.count("*").alias("game_count"),
            F.round(F.sum(column_name), 2).alias("regional_sales")
        )

        region_df = (
            current_region if region_df is None
            else region_df.unionByName(current_region)
        )

    return region_df


def top_selling_games(df: DataFrame, limit: int = 10) -> DataFrame:
    """Return the highest-selling games."""

    return (
        df
        .select(
            "rank",
            "name",
            "platform",
            "year",
            "genre",
            "publisher",
            "global_sales"
        )
        .orderBy(F.desc("global_sales"))
        .limit(limit)
    )
