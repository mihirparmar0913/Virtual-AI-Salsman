import json

import pandas as pd


REQUIRED_COLUMNS = {
    "Category",
    "Full Product Name",
    "Brand",
    "Price",
    "Description",
    "Features",
    "Rating",
    "Review Count",
    "Availability",
    "High Resolution Image",
    "Main Category",
    "Product Category",
    "Price Numeric",
    "Review Count Numeric",
    "Search Text",
}


def validate_required_columns(dataframe: pd.DataFrame) -> None:
    """Validate that all required columns are present."""

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )


def validate_not_empty(dataframe: pd.DataFrame) -> None:
    """Validate that the dataset contains at least one row."""

    if dataframe.empty:
        raise ValueError("Dataset is empty.")


def validate_prices(dataframe: pd.DataFrame) -> None:
    """Validate that product prices are positive."""

    invalid_prices = dataframe["Price Numeric"].isna() | (
        dataframe["Price Numeric"] <= 0
    )

    if invalid_prices.any():
        count = int(invalid_prices.sum())
        raise ValueError(
            f"Found {count} products with invalid prices."
        )


def validate_ratings(dataframe: pd.DataFrame) -> None:
    """Validate ratings when they are available."""

    ratings = dataframe["Rating"].dropna()

    invalid_ratings = (ratings < 0) | (ratings > 5)

    if invalid_ratings.any():
        raise ValueError(
            "Found ratings outside the valid 0-5 range."
        )


def validate_review_counts(dataframe: pd.DataFrame) -> None:
    """Validate review counts when they are available."""

    review_counts = dataframe["Review Count Numeric"].dropna()

    if (review_counts < 0).any():
        raise ValueError(
            "Found negative review counts."
        )


def validate_features_json(dataframe: pd.DataFrame) -> None:
    """Validate that every Features value contains valid JSON."""

    invalid_rows = []

    for index, value in dataframe["Features"].items():
        try:
            json.loads(value)
        except (TypeError, json.JSONDecodeError):
            invalid_rows.append(index)

    if invalid_rows:
        raise ValueError(
            f"Found {len(invalid_rows)} rows with invalid Features JSON."
        )


def validate_product_data(dataframe: pd.DataFrame) -> None:
    """Run all product dataset validation checks."""

    validate_not_empty(dataframe)
    validate_required_columns(dataframe)
    validate_prices(dataframe)
    validate_ratings(dataframe)
    validate_review_counts(dataframe)
    validate_features_json(dataframe)