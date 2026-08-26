from src.data_processing.loader import load_product_data


DATA_PATH = "data/raw/amazon_final_ai_sales_assistant_dataset.csv"
# DATA_PATH = "data/raw/wrong_file.csv"


def test_load_product_data():
    dataframe = load_product_data(DATA_PATH)

    assert dataframe is not None
    assert not dataframe.empty

    print("\nDataset loaded successfully!")
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Columns: {dataframe.shape[1]}")


if __name__ == "__main__":
    test_load_product_data()