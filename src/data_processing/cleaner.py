import re

import pandas as pd


TEXT_COLUMNS = [
    "Category",
    "Full Product Name",
    "Brand",
    "Description",
    "Availability",
    "Main Category",
    "Category Level 2",
    "Category Level 3",
    "Category Level 4",
    "Category Level 5",
    "Category Level 6",
    "Category Level 7",
    "Category Level 8",
    "Product Category",
    "Search Text",
]


def clean_text(value):
    """Normalize a text value while preserving meaningful content."""

    if pd.isna(value):
        return None

    value = str(value)

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value)

    # Remove leading/trailing whitespace
    value = value.strip()

    return value if value else None


def clean_text_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean text fields in the product dataset."""

    dataframe = dataframe.copy()

    for column in TEXT_COLUMNS:
        if column in dataframe.columns:
            dataframe[column] = dataframe[column].apply(clean_text)

    return dataframe


def clean_numeric_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Ensure numeric fields contain numeric values."""

    dataframe = dataframe.copy()

    dataframe["Price Numeric"] = pd.to_numeric(
        dataframe["Price Numeric"],
        errors="coerce",
    )

    dataframe["Rating"] = pd.to_numeric(
        dataframe["Rating"],
        errors="coerce",
    )

    dataframe["Review Count Numeric"] = pd.to_numeric(
        dataframe["Review Count Numeric"],
        errors="coerce",
    )

    return dataframe


def normalize_availability(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normalize availability values."""

    dataframe = dataframe.copy()

    if "Availability" in dataframe.columns:
        dataframe["Availability"] = (
            dataframe["Availability"]
            .str.strip()
            .str.lower()
        )

    return dataframe


def clean_product_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Run the basic cleaning pipeline.

    This function does not perform deduplication.
    Duplicate handling is intentionally separated.
    """

    cleaned = dataframe.copy()

    cleaned = clean_text_columns(cleaned)
    cleaned = clean_numeric_columns(cleaned)
    cleaned = normalize_availability(cleaned)

    return cleaned