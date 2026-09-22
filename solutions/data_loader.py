"""Mentor reference — complete data loading (do not share with students until showcase)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.kaggle_schema import COL_PARTICIPANT, KAGGLE_FILENAME, LABEL_FATIGUE
from solutions.features import build_features_from_kaggle, fatigue_label

REPO_ROOT = Path(__file__).resolve().parents[1]
KAGGLE_RAW = REPO_ROOT / "data" / "kaggle" / KAGGLE_FILENAME
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
DEFAULT_PROCESSED = REPO_ROOT / "data" / "processed" / "features_v1.csv"


def load_kaggle_raw(path: Path | None = None) -> pd.DataFrame:
    path = path or KAGGLE_RAW
    if not path.exists():
        raise FileNotFoundError(
            f"Download the Kaggle CSV to {path}. See docs/KAGGLE_SETUP.md."
        )
    return pd.read_csv(path)


def load_feature_table(use_demo: bool = False) -> pd.DataFrame:
    if not use_demo and DEFAULT_PROCESSED.exists():
        df = pd.read_csv(DEFAULT_PROCESSED)
    elif not use_demo and KAGGLE_RAW.exists():
        raw = load_kaggle_raw()
        df = build_features_from_kaggle(raw)
        df[LABEL_FATIGUE] = fatigue_label(df)
    elif DEFAULT_DEMO.exists():
        df = pd.read_csv(DEFAULT_DEMO)
    else:
        raise FileNotFoundError("No data found. See docs/KAGGLE_SETUP.md or run generate_demo_data.py.")

    if LABEL_FATIGUE not in df.columns:
        raise ValueError(f"Missing label column `{LABEL_FATIGUE}`.")
    return df


def participant_groups(df: pd.DataFrame) -> pd.Series:
    if COL_PARTICIPANT in df.columns:
        return df[COL_PARTICIPANT].astype(str)
    return pd.Series(range(len(df)), index=df.index)
