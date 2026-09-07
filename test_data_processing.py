# import pandas as pd
# from src.data_processing.feature_analyzer import (
#     extract_feature_keys,
#     get_feature_frequency,
#     get_feature_frequency_by_category,
#     normalize_feature_name,
#     find_formatting_aliases,
#     extract_feature_keys_and_values,
#     get_feature_value_frequency,
#     get_category_feature_profile,
#     get_category_feature_profile,
# )

# def test_extract_feature_keys_and_values():
#     value = '{"RAM": "16 GB", "Storage": "512 GB"}'

#     result = extract_feature_keys_and_values(value)

#     assert result == [
#         ("RAM", "16 GB"),
#         ("Storage", "512 GB"),
#     ]


# def test_get_feature_value_frequency():
#     df = pd.DataFrame(
#         {
#             "Features": [
#                 '{"RAM": "16 GB"}',
#                 '{"RAM": "16 GB"}',
#                 '{"RAM": "8 GB"}',
#             ]
#         }
#     )

#     result = get_feature_value_frequency(
#         df,
#         features=["RAM"],
#     )

#     ram_16 = result[
#         (result["feature"] == "RAM")
#         & (result["value"] == "16 GB")
#     ].iloc[0]

#     ram_8 = result[
#         (result["feature"] == "RAM")
#         & (result["value"] == "8 GB")
#     ].iloc[0]

#     assert ram_16["frequency"] == 2
#     assert ram_8["frequency"] == 1
# def test_get_category_feature_profile():
#     df = pd.DataFrame(
#         {
#             "Main Category": [
#                 "Electronics",
#                 "Electronics",
#                 "Electronics",
#                 "Electronics",
#             ],
#             "Features": [
#                 '{"RAM": "8 GB", "Colour": "Black"}',
#                 '{"RAM": "16 GB", "Colour": "White"}',
#                 '{"RAM": "8 GB", "Colour": "Black"}',
#                 '{"RAM": "16 GB"}',
#             ],
#         }
#     )

#     result = get_category_feature_profile(
#         df,
#         min_percentage=50.0,
#     )

#     ram = result[
#         (result["main_category"] == "Electronics")
#         & (result["feature"] == "RAM")
#     ]

#     colour = result[
#         (result["main_category"] == "Electronics")
#         & (result["feature"] == "Colour")
#     ]

#     assert len(ram) == 1
#     assert ram.iloc[0]["percentage"] == 100.0

#     assert len(colour) == 1
#     assert colour.iloc[0]["percentage"] == 75.0

# # --------------------------------------------------
# # 5. Category feature profiles
# # --------------------------------------------------

# category_profiles = get_category_feature_profile(
#     df,
#     min_percentage=10.0,
# )

# category_profiles.to_csv(
#     OUTPUT_DIR / "category_feature_profiles.csv",
#     index=False,
# )

# print("\nCategory Feature Profiles:")

# for category in category_profiles["main_category"].unique():
#     category_features = category_profiles[
#         category_profiles["main_category"] == category
#     ]

#     print(f"\n{category}:")
#     print(
#         category_features[
#             ["feature", "frequency", "percentage"]
#         ].to_string(index=False)
#     )

from src.data_processing.category_schema import (
    get_category_schema,
    is_supported_category,
)
def test_get_category_schema():
    schema = get_category_schema("laptop")

    assert "ram_gb" in schema
    assert "processor" in schema
    assert "processor_speed_ghz" in schema


def test_running_shoes_schema():
    schema = get_category_schema("running_shoes")

    assert "material" in schema
    assert "sole_material" in schema
    assert "closure_type" in schema
    assert "heel_type" in schema


def test_supported_category():
    assert is_supported_category("laptop") is True
    assert is_supported_category("running_shoes") is True
    assert is_supported_category("unknown_category") is False


def test_unknown_category_returns_empty_schema():
    assert get_category_schema("unknown_category") == []