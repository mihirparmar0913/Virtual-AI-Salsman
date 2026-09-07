"""
Canonical feature schema for supported product categories.

This schema defines the features our recommendation system
will understand and use for filtering, ranking, and comparison.
"""


CATEGORY_SCHEMAS = {
    "smartphone": [
        "ram_gb",
        "storage",
        "operating_system",
        "processor",
        "processor_speed_ghz",
        "battery_capacity_mah",
        "display",
        "camera",
        "colour",
    ],

    "laptop": [
        "ram_gb",
        "storage",
        "processor",
        "processor_speed_ghz",
        "operating_system",
        "display",
        "graphics",
        "colour",
    ],

    "headphones": [
        "connectivity",
        "audio_output_mode",
        "ear_placement",
        "special_features",
        "colour",
    ],

    "speaker": [
        "connectivity",
        "speaker_output_power_w",
        "audio_output_mode",
        "special_features",
        "colour",
    ],

    "watch": [
        "watch_movement",
        "band_material",
        "band_colour",
        "case_diameter",
        "water_resistance",
        "colour",
    ],

    "running_shoes": [
        "material",
        "sole_material",
        "closure_type",
        "heel_type",
        "colour",
    ],

    "shirt": [
        "material",
        "fit",
        "colour",
        "style",
        "closure_type",
    ],

    "tshirt": [
        "material",
        "fit",
        "colour",
        "style",
    ],

    "bag": [
        "material",
        "colour",
        "style",
        "capacity",
        "closure_type",
    ],
}


COMMON_FEATURES = [
    "brand",
    "colour",
]


def get_category_schema(category):
    """
    Return the canonical features supported for a category.

    Args:
        category: Canonical category name.

    Returns:
        list[str]: Supported canonical features.
    """
    return CATEGORY_SCHEMAS.get(category, [])


def is_supported_category(category):
    """
    Check whether a category has a defined schema.
    """
    return category in CATEGORY_SCHEMAS