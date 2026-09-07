import pandas as pd
from src.data_processing.feature_analyzer import (
    extract_feature_keys,
    get_feature_frequency,
    get_feature_frequency_by_category,
    normalize_feature_name,
    find_formatting_aliases,
)
def test_extract_feature_keys():
    value = '{"RAM": "16 GB", "Storage": "512 GB"}'

    result = extract_feature_keys(value)

    assert result == ["RAM", "Storage"]


def test_extract_feature_keys_invalid_json():
    value = '{"RAM": "16 GB"'

    result = extract_feature_keys(value)

    assert result == []


def test_normalize_feature_name():
    assert normalize_feature_name("Battery Type") == "battery type"
    assert normalize_feature_name("Battery-Type") == "battery type"
    assert normalize_feature_name("  Battery   Type  ") == "battery type"


def test_get_feature_frequency():
    df = pd.DataFrame(
        {
            "Features": [
                '{"RAM": "16 GB", "Storage": "512 GB"}',
                '{"RAM": "8 GB"}',
                '{"Storage": "1 TB"}',
            ]
        }
    )

    result = get_feature_frequency(df)

    ram = result[result["feature"] == "RAM"].iloc[0]
    storage = result[result["feature"] == "Storage"].iloc[0]

    assert ram["frequency"] == 2
    assert storage["frequency"] == 2


def test_get_feature_frequency_by_category():
    df = pd.DataFrame(
        {
            "Main Category": [
                "Electronics",
                "Electronics",
                "Clothing & Accessories",
            ],
            "Features": [
                '{"RAM": "16 GB"}',
                '{"RAM": "8 GB"}',
                '{"Material": "Cotton"}',
            ],
        }
    )

    result = get_feature_frequency_by_category(df)

    ram = result[
        (result["main_category"] == "Electronics")
        & (result["feature"] == "RAM")
    ].iloc[0]

    assert ram["frequency"] == 2
    assert ram["percentage"] == 100.0


def test_find_formatting_aliases():
    df = pd.DataFrame(
        {
            "feature": [
                "Battery Type",
                "Battery type",
                "RAM",
            ],
            "frequency": [100, 50, 80],
        }
    )

    result = find_formatting_aliases(df)

    assert len(result) == 1
    assert result.iloc[0]["normalized_feature"] == "battery type"