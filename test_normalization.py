import pandas as pd

from src.data_processing.feature_parser import parse_and_normalize_features
from src.data_processing.feature_normalizer import normalize_feature_value


df = pd.read_csv(
    "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
)

categories = [
    "Smartphones",
    "Traditional Laptops",
    "Over-Ear",
    "Running Shoes",
    "Wrist Watches",
]

for category in categories:
    products = df[df["Product Category"] == category]

    if products.empty:
        print(f"\n❌ No product found for: {category}")
        continue

    product = products.iloc[0]

    print("\n" + "=" * 80)
    print(f"Category: {category}")
    print(f"Product: {product['Full Product Name']}")

    print("\nRaw Features:")
    print(product["Features"])

    normalized = parse_and_normalize_features(product["Features"])

    print("\nNormalized Features:")
    print(normalized)