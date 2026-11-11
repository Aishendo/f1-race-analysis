from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent


def load_race_table(table_name: str) -> pd.DataFrame:
    """Load a saved Monza 2024 table.

    Args:
        table_name: One of drivers, laps, stints, race_control,
            or session_result.

    Returns:
        A DataFrame containing the saved data.

    Raises:
        ValueError: If the table name is unsupported.
        FileNotFoundError: If the CSV file does not exist.
    """
    allowed_tables = {
        "drivers",
        "laps",
        "stints",
        "race_control",
        "session_result",
    }

    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table: {table_name}")

    file_path = (
        PROJECT_DIR / "data" / "raw"
        / f"monza_2024_{table_name}.csv"
    )

    if not file_path.is_file():
        raise FileNotFoundError(f"Missing data file: {file_path}")

    return pd.read_csv(file_path)