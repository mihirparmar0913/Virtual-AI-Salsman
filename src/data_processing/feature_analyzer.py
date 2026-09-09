import json
from collections import Counter, defaultdict

import pandas as pd


def extract_feature_keys(value):
    """
    Extract feature names from a Features JSON value.

    Returns:
        list[str]: Feature keys found in the value.
    """
    if value is None or pd.isna(value):
        return []

    if isinstance(value, dict):
        return list(value.keys())

    if isinstance(value, str):
        try:
            parsed = json.loads(value)

            if isinstance(parsed, dict):
                return list(parsed.keys())

        except (json.JSONDecodeError, TypeError):
            return []

    return []


def get_feature_frequency(df):
    """
    Count how frequently each feature appears in the dataset.

    Returns:
        pd.DataFrame with columns:
        - feature
        - frequency
        - percentage
    """
    counter = Counter()

    for value in df["Features"]:
        counter.update(extract_feature_keys(value))

    total_products = len(df)

    results = [
        {
            "feature": feature,
            "frequency": frequency,
            "percentage": round((frequency / total_products) * 100, 2),
        }
        for feature, frequency in counter.items()
    ]

    return (
        pd.DataFrame(results)
        .sort_values("frequency", ascending=False)
        .reset_index(drop=True)
    )


def get_feature_frequency_by_category(df):
    """
    Calculate feature frequency for each main product category.

    Returns:
        pd.DataFrame with:
        - main_category
        - feature
        - frequency
        - percentage
    """
    category_feature_counter = defaultdict(Counter)
    category_product_count = df["Main Category"].value_counts().to_dict()

    for _, row in df.iterrows():
        category = row["Main Category"]
        features = extract_feature_keys(row["Features"])

        category_feature_counter[category].update(features)

    results = []

    for category, feature_counter in category_feature_counter.items():
        product_count = category_product_count[category]

        for feature, frequency in feature_counter.items():
            results.append(
                {
                    "main_category": category,
                    "feature": feature,
                    "frequency": frequency,
                    "percentage": round(
                        (frequency / product_count) * 100, 2
                    ),
                }
            )

    return (
        pd.DataFrame(results)
        .sort_values(
            ["main_category", "frequency"],
            ascending=[True, False],
        )
        .reset_index(drop=True)
    )


def normalize_feature_name(feature):
    """
    Create a simple normalized version of a feature name.

    This is intentionally conservative.

    It only normalizes formatting differences such as:
    - uppercase/lowercase
    - extra spaces
    - hyphens
    - underscores

    It does NOT perform semantic mapping.
    """
    if not isinstance(feature, str):
        return ""

    normalized = feature.strip().lower()

    normalized = normalized.replace("-", " ")
    normalized = normalized.replace("_", " ")

    normalized = " ".join(normalized.split())

    return normalized


def find_formatting_aliases(feature_frequency):
    """
    Find feature names that become identical after
    basic formatting normalization.

    Example:
        Battery Type
        Battery type

    Both become:
        battery type
    """
    aliases = defaultdict(list)

    for feature in feature_frequency["feature"]:
        normalized = normalize_feature_name(feature)
        aliases[normalized].append(feature)

    results = []

    for normalized, variants in aliases.items():
        if len(variants) > 1:
            results.append(
                {
                    "normalized_feature": normalized,
                    "variants": variants,
                    "variant_count": len(variants),
                }
            )

    return (
        pd.DataFrame(results)
        .sort_values("variant_count", ascending=False)
        .reset_index(drop=True)
    )
def get_feature_value_frequency(df, features=None):
    """
    Count how frequently each value occurs for each feature.

    Args:
        df: Product DataFrame.
        features: Optional list of feature names to analyze.
                  If None, all features are analyzed.

    Returns:
        pd.DataFrame with:
        - feature
        - value
        - frequency
    """
    counter = Counter()

    for raw_features in df["Features"]:
        feature_data = extract_feature_keys_and_values(raw_features)

        for feature, value in feature_data:
            if features is None or feature in features:
                counter[(feature, value)] += 1

    results = [
        {
            "feature": feature,
            "value": value,
            "frequency": frequency,
        }
        for (feature, value), frequency in counter.items()
    ]

    return (
        pd.DataFrame(results)
        .sort_values(
            ["feature", "frequency"],
            ascending=[True, False],
        )
        .reset_index(drop=True)
    )


def extract_feature_keys_and_values(value):
    """
    Extract feature key-value pairs from a Features JSON value.

    Returns:
        list[tuple]: List of (feature, value) pairs.
    """
    if value is None or pd.isna(value):
        return []

    if isinstance(value, dict):
        parsed = value

    elif isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []

        if not isinstance(parsed, dict):
            return []

    else:
        return []

    return [
        (str(feature).strip(), str(feature_value).strip())
        for feature, feature_value in parsed.items()
    ]
def get_category_feature_profile(df, min_percentage=10.0):
    """
    Identify features that appear frequently within each product category.

    Args:
        df: Product DataFrame.
        min_percentage: Minimum percentage of products in a category
                        that must contain the feature.

    Returns:
        pd.DataFrame containing:
        - main_category
        - feature
        - frequency
        - percentage
    """
    category_frequency = get_feature_frequency_by_category(df)

    profile = category_frequency[
        category_frequency["percentage"] >= min_percentage
    ].copy()

    return profile.sort_values(
        ["main_category", "percentage"],
        ascending=[True, False],
    ).reset_index(drop=True)
    