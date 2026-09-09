from pathlib import Path

from src.data_processing.loader import load_product_data
from src.data_processing.cleaner import clean_product_data
from src.database.ingestion import generate_product_id


RAW_DATA_PATH = Path(
    "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
)

df = load_product_data(RAW_DATA_PATH)
df = clean_product_data(df)

df["generated_id"] = df.apply(
    generate_product_id,
    axis=1,
)

duplicate_ids = df[
    df["generated_id"].duplicated(keep=False)
].sort_values("generated_id")

print(f"Total products: {len(df)}")
print(f"Unique generated IDs: {df['generated_id'].nunique()}")
print(f"Duplicate ID rows: {len(duplicate_ids)}")
print(f"Duplicate ID groups: {duplicate_ids['generated_id'].nunique()}")

print("\nDuplicate records:")
print(
    duplicate_ids[
        [
            "generated_id",
            "Full Product Name",
            "Brand",
            "Price Numeric",
            "Description",
        ]
    ].to_string(index=False)
)