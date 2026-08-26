from pathlib import Path

import pandas as pd


def load_product_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load the raw product dataset from a CSV file.

    Args:
        file_path: Path to the raw CSV dataset.

    Returns:
        A pandas DataFrame containing the raw product data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            f"Expected a CSV file, got: {file_path.suffix}"
        )

    try:
        dataframe = pd.read_csv(file_path)
    except Exception as error:
        raise RuntimeError(
            f"Failed to load dataset: {file_path}"
        ) from error

    if dataframe.empty:
        raise ValueError(
            "The dataset is empty."
        )

    return dataframe