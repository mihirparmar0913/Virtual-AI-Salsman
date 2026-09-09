import hashlib
import uuid
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from src.data_processing.loader import load_product_data
from src.data_processing.cleaner import clean_product_data
from src.data_processing.feature_parser import parse_and_normalize_features
from src.database.connection import SessionLocal
from src.database.models import Product


RAW_DATA_PATH = Path(
    "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
)


def generate_product_id(row: pd.Series, row_index: int) -> uuid.UUID:
    """
    Generate a deterministic UUID for a source CSV row.

    The source row index ensures that even exact duplicate
    records receive different product IDs.
    """
    source = "|".join(
        [
            str(row_index),
            str(row.get("Full Product Name", "")),
            str(row.get("Brand", "")),
            str(row.get("Price Numeric", "")),
            str(row.get("Description", "")),
        ]
    )

    hash_value = hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()

    return uuid.uuid5(
        uuid.NAMESPACE_URL,
        hash_value,
    )
def _clean_val(val, target_type=str):
    if pd.isna(val):
        return None
    if target_type == int:
        return int(val)
    if target_type == float:
        return float(val)
    return str(val)


def prepare_product_record(
    row: pd.Series,
    row_index: int,
) -> dict:
    """
    Convert one cleaned CSV row into a database-ready product record.
    """
    return {
        "product_id": generate_product_id(
            row,
            row_index,
        ),
        "product_name": _clean_val(row["Full Product Name"], str),
        "brand": _clean_val(row["Brand"], str),
        "main_category": _clean_val(row["Main Category"], str),
        "category_level_2": _clean_val(row["Category Level 2"], str),
        "category_level_3": _clean_val(row["Category Level 3"], str),
        "product_category": _clean_val(row["Product Category"], str),
        "price": _clean_val(row["Price Numeric"], float),
        "rating": _clean_val(row["Rating"], float),
        "review_count": _clean_val(row["Review Count Numeric"], int),
        "availability": _clean_val(row["Availability"], str),
        "description": _clean_val(row["Description"], str),
        "features": parse_and_normalize_features(
            row["Features"]
        ),
        "image_url": _clean_val(row["Image URL"], str),
        "embedding_text": None,
        "embedding": None,
    }


def ingest_products() -> int:
    """
    Load, clean, normalize and insert products into PostgreSQL.

    Returns the number of newly inserted products.
    """
    df = load_product_data(RAW_DATA_PATH)
    df = clean_product_data(df)

    records = [
    prepare_product_record(row, row_index)
    for row_index, row in df.iterrows()
]

    inserted_count = 0

    with SessionLocal() as session:
        existing_ids = set(
            session.scalars(
                select(Product.product_id)
            ).all()
        )

        new_records = [
            record
            for record in records
            if record["product_id"] not in existing_ids
        ]

        if new_records:
            session.add_all(
                [
                    Product(**record)
                    for record in new_records
                ]
            )

            session.commit()

        inserted_count = len(new_records)

    return inserted_count


if __name__ == "__main__":
    count = ingest_products()

    print(
        f"Inserted {count} new products into PostgreSQL."
    )