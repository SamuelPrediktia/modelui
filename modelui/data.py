import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from .googlevision import ImageUri

DATA_FOLDER = Path(__file__).parent / "resources"
THUMBNAILS_BUCKET = os.getenv("THUMBNAILS_BUCKET")


def get_predictions():
    return pd.read_parquet(DATA_FOLDER / "predictions_margins.parquet")


def get_matches():
    return pd.read_parquet(DATA_FOLDER / "matches_margins.parquet")


def load_thumbnail(
    sku: str,
    catalog: str = "freeport",
    size: str = "medium",
):
    uri = f"gs://{THUMBNAILS_BUCKET}/{catalog}/{size}/{sku}.jpg"
    return ImageUri(uri).load()
