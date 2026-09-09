from pathlib import Path

from src.data_processing.loader import load_product_data
from src.data_processing.feature_analyzer import (
    get_feature_frequency,
    get_feature_frequency_by_category,
    find_formatting_aliases,
    get_feature_value_frequency,
)
# Path to the raw dataset
DATA_PATH = Path(
    "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
)

# Directory where analysis reports will be saved
OUTPUT_DIR = Path("data/metadata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Load dataset
df = load_product_data(DATA_PATH)

print(f"Products: {len(df)}")


# --------------------------------------------------
# 1. Overall feature frequency
# --------------------------------------------------

feature_frequency = get_feature_frequency(df)

feature_frequency.to_csv(
    OUTPUT_DIR / "feature_frequency.csv",
    index=False,
)

print("\nTop 30 features:")
print(
    feature_frequency.head(30).to_string(index=False)
)


# --------------------------------------------------
# 2. Feature frequency by category
# --------------------------------------------------

category_frequency = get_feature_frequency_by_category(df)

category_frequency.to_csv(
    OUTPUT_DIR / "feature_frequency_by_category.csv",
    index=False,
)

print("\nFeature frequency by category:")
print(
    category_frequency.head(50).to_string(index=False)
)


# --------------------------------------------------
# 3. Formatting aliases
# --------------------------------------------------

aliases = find_formatting_aliases(feature_frequency)

aliases.to_json(
    OUTPUT_DIR / "feature_formatting_aliases.json",
    orient="records",
    indent=2,
)

print("\nFormatting aliases:")

if aliases.empty:
    print("No formatting aliases found.")
else:
    print(
        aliases.to_string(index=False)
    )


print("\nAnalysis completed successfully.")
print(f"Reports saved to: {OUTPUT_DIR}")
# --------------------------------------------------
# 4. Feature value frequency
# --------------------------------------------------

important_features = [
    "Brand",
    "Colour",
    "RAM Memory Installed Size",
    "Operating System",
    "CPU Model",
    "CPU Speed",
    "Material",
    "Material type",
    "Closure type",
    "Closure Type",
    "Heel type",
    "Sole material",
    "Water resistance level",
    "Connectivity Technology",
    "Watch movement type",
    "Band material type",
    "Fit type",
]

value_frequency = get_feature_value_frequency(
    df,
    features=important_features,
)

value_frequency.to_csv(
    OUTPUT_DIR / "feature_value_frequency.csv",
    index=False,
)

print("\nTop feature values:")

for feature in important_features:
    feature_values = value_frequency[
        value_frequency["feature"] == feature
    ].head(10)

    if not feature_values.empty:
        print(f"\n{feature}:")
        print(
            feature_values.to_string(index=False)
        )