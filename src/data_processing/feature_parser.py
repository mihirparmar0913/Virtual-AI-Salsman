import json
from typing import Any
from src.data_processing.feature_normalizer import (
    normalize_feature_name,
    normalize_feature_value,
)

def parse_features(value: Any) -> dict:
    """
    Parse a product Features value into a dictionary.

    Args:
        value: JSON string, dictionary, or missing value.

    Returns:
        Parsed feature dictionary.

    Raises:
        ValueError: If the value cannot be parsed as a dictionary.
    """

    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    if not isinstance(value, str):
        raise ValueError(
            f"Expected Features to be a string or dictionary, "
            f"got {type(value).__name__}"
        )

    value = value.strip()

    if not value:
        return {}

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Invalid JSON in Features field"
        ) from error

    if not isinstance(parsed, dict):
        raise ValueError(
            "Features JSON must contain an object/dictionary"
        )

    return parsed


def normalize_feature_keys(features: dict) -> dict:
    """
    Normalize feature keys while preserving their meaning.
    """

    normalized = {}

    for key, value in features.items():

        clean_key = str(key).strip()

        if not clean_key:
            continue

        normalized[clean_key] = value

    return normalized


def parse_and_normalize_features(value: Any) -> dict:
    """
    Parse and normalize a product's Features field.
    """

    features = parse_features(value)

    return normalize_feature_keys(features)

def normalize_feature_keys(features: dict) -> dict:
    """
    Normalize feature names and values using the canonical feature schema.
    """

    normalized = {}

    for key, value in features.items():

        clean_key = str(key).strip()

        if not clean_key:
            continue

        canonical_name = normalize_feature_name(clean_key)

        if canonical_name is None:
            continue

        normalized_value = normalize_feature_value(
            canonical_name,
            value
        )

        if normalized_value is None:
            continue

        normalized[canonical_name] = normalized_value

    return normalized    