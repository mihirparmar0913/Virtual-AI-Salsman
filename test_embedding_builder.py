from pathlib import Path

from src.data_processing.loader import load_product_data
from src.data_processing.cleaner import clean_product_data
from src.data_processing.feature_parser import parse_and_normalize_features
from src.data_processing.embedding_builder import build_embedding_text


RAW_DATA_PATH = Path(
    "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
)

df = load_product_data(RAW_DATA_PATH)
df = clean_product_data(df)

for index, row in df.head(5).iterrows():

    product = {
        "product_name": row["Full Product Name"],
        "brand": row["Brand"],
        "main_category": row["Main Category"],
        "product_category": row["Product Category"],
        "description": row["Description"],
        "features": parse_and_normalize_features(
            row["Features"]
        ),
    }

    print("=" * 80)
    print(f"Product #{index + 1}")
    print(build_embedding_text(product))