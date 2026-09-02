from src.data_processing.loader import load_product_data
from src.data_processing.validator import validate_product_data
from src.data_processing.cleaner import clean_product_data


DATA_PATH = "data/raw/amazon_final_ai_sales_assistant_dataset.csv"


def test_product_data():
    dataframe = load_product_data(DATA_PATH)

    validate_product_data(dataframe)

    cleaned_dataframe = clean_product_data(dataframe)

    assert len(cleaned_dataframe) == len(dataframe)

    assert cleaned_dataframe["Price Numeric"].dtype.kind in "fi"
    assert cleaned_dataframe["Rating"].dtype.kind in "fi"

    print("\nDataset validation passed!")
    print(f"Raw rows: {len(dataframe)}")
    print(f"Cleaned rows: {len(cleaned_dataframe)}")

    print("\nAvailability values:")
    print(cleaned_dataframe["Availability"].value_counts())


if __name__ == "__main__":
    test_product_data()