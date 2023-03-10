import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from .googlevision import ImageUri

DATA_FOLDER = Path(__file__).parent / "resources"
THUMBNAILS_BUCKET = os.getenv("THUMBNAILS_BUCKET")


def get_predictions(approach: str):
    if approach=='coventional':
        return pd.read_parquet(DATA_FOLDER / "predictions_margins.parquet")
    elif approach=='consistent-weighted':
        return pd.read_parquet(DATA_FOLDER / "predictions_margins_weighted.parquet")
    elif approach=='likelihood':
        return pd.read_parquet(DATA_FOLDER / "predictions_margins_likelihood.parquet")



def get_matches(approach: str):
    if approach=='coventional':
        return pd.read_parquet(DATA_FOLDER / "matches_margins.parquet")
    elif approach=='consistent-weighted':
        return pd.read_parquet(DATA_FOLDER / "matches_margins_weighted.parquet")
    elif approach=='likelihood':
        return pd.read_parquet(DATA_FOLDER / "matches_margins_likelihood.parquet")


def load_thumbnail(
    sku: str,
    catalog: str = "freeport",
    size: str = "medium",
):
    uri = f"gs://{THUMBNAILS_BUCKET}/{catalog}/{size}/{sku}.jpg"
    return ImageUri(uri).load()
