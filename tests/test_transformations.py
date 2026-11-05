
from datetime import datetime

from src.transformations.silver import transform_silver


def test_silver_transformation(spark):
    columns = [
        "Rank", "Name", "Platform", "Year",
        "Genre", "Publisher", "NA_Sales",
        "EU_Sales", "JP_Sales", "Other_Sales",
        "Global_Sales", "source_file",
        "ingestion_timestamp"
    ]

    records = [
        (
            1, " Game A ", "PS3", "2012",
            "Action", "Publisher A",
            1.0, 0.5, 0.2, 0.1, 1.8,
            "test.csv", datetime(2026, 1, 1)
        ),
        (
            2, "Game B", "Wii", "N/A",
            "Shooter", "Publisher B",
            1.0, 0.0, 0.0, 0.0, 1.0,
            "test.csv", datetime(2026, 1, 1)
        )
    ]

    bronze_df = spark.createDataFrame(records, columns)

    silver_df = transform_silver(bronze_df)

    assert silver_df.count() == 2

    game_a = silver_df.filter("rank = 1").first()

    assert game_a["name"] == "Game A"
    assert game_a["year"] == 2012
    assert game_a["year_status"] == "VALID"
    assert game_a["regional_sales_total"] == 1.8
    assert game_a["sales_reconciliation_status"] == "MATCH"

    game_b = silver_df.filter("rank = 2").first()

    assert game_b["year"] is None
    assert game_b["year_status"] == "MISSING_OR_INVALID"
