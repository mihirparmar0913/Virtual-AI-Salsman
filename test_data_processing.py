from src.data_processing.loader import load_product_data
from src.data_processing.validator import validate_product_data


DATA_PATH = "data/raw/amazon_final_ai_sales_assistant_dataset.csv"


def test_product_data():
    dataframe = load_product_data(DATA_PATH)

    validate_product_data(dataframe)

    assert len(dataframe) == 2171

    print("\nDataset validation passed!")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")


if __name__ == "__main__":
    test_product_data()