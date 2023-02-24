from pathlib import Path

import pandas as pd

DATA_FOLDER = Path(__file__).parent / "resources"


def get_predictions():
    return pd.read_parquet(DATA_FOLDER / "predictions.parquet")


def get_matches():
    return pd.read_parquet(DATA_FOLDER / "matches.parquet")
