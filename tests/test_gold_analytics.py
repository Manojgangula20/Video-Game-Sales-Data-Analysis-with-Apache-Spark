import pytest

from src.analytics.gold import (
    sales_by_year,
    sales_by_platform,
    sales_by_genre,
    regional_sales,
    top_selling_games,
)


@pytest.fixture
def sales_df(spark):
    records = [
        (1, "Game A", "PS3", 2012, "Action", "Pub A",
         1.0, 0.5, 0.2, 0.1, 1.8),
        (2, "Game B", "Wii", 2010, "Sports", "Pub B",
         2.0, 1.0, 0.5, 0.5, 4.0),
        (3, "Game C", "PS3", None, "Action", "Pub A",
         0.5, 0.2, 0.1, 0.2, 1.0),
    ]

    columns = [
        "rank", "name", "platform", "year", "genre", "publisher",
        "na_sales", "eu_sales", "jp_sales", "other_sales",
        "global_sales"
    ]

    return spark.createDataFrame(records, columns)


def test_sales_by_year_preserves_unknown_year(sales_df):
    result = sales_by_year(sales_df)

    rows = {
        row["release_year"]: row
        for row in result.collect()
    }

    assert len(rows) == 3
    assert rows["2012"]["game_count"] == 1
    assert rows["2010"]["global_sales"] == 4.0
    assert rows["UNKNOWN"]["game_count"] == 1


def test_sales_by_platform_aggregates_correctly(sales_df):
    result = sales_by_platform(sales_df)

    rows = {
        row["platform"]: row
        for row in result.collect()
    }

    assert rows["PS3"]["game_count"] == 2
    assert rows["PS3"]["global_sales"] == 2.8
    assert rows["Wii"]["global_sales"] == 4.0


def test_sales_by_genre_aggregates_correctly(sales_df):
    result = sales_by_genre(sales_df)

    rows = {
        row["genre"]: row
        for row in result.collect()
    }

    assert rows["Action"]["game_count"] == 2
    assert rows["Action"]["global_sales"] == 2.8
    assert rows["Sports"]["global_sales"] == 4.0


def test_regional_sales_returns_four_regions(sales_df):
    result = regional_sales(sales_df)

    rows = {
        row["region"]: row
        for row in result.collect()
    }

    assert set(rows.keys()) == {"NA", "EU", "JP", "OTHER"}

    assert all(
        row["game_count"] == 3
        for row in rows.values()
    )

    assert rows["NA"]["regional_sales"] == 3.5
    assert rows["EU"]["regional_sales"] == 1.7
    assert rows["JP"]["regional_sales"] == 0.8
    assert rows["OTHER"]["regional_sales"] == 0.8


def test_top_selling_games_respects_limit(sales_df):
    result = top_selling_games(sales_df, limit=2)

    rows = result.collect()

    assert len(rows) == 2
    assert rows[0]["name"] == "Game B"
    assert rows[1]["name"] == "Game A"
    assert "global_sales" in result.columns
