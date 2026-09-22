"""Load feature tables + person baselines."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from solutions.baselines import compute_person_baselines
from solutions.features import build_features_from_kaggle, strain_label
from src.kaggle_schema import COL_PARTICIPANT, KAGGLE_FILENAME, LABEL_STRAIN

REPO_ROOT = Path(__file__).resolve().parents[1]
KAGGLE_RAW = REPO_ROOT / "data" / "kaggle" / KAGGLE_FILENAME
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
BASELINES_DEMO = REPO_ROOT / "data" / "person_baselines.csv"
DEFAULT_PROCESSED = REPO_ROOT / "data" / "processed" / "features_v1.csv"


def load_kaggle_raw(path: Path | None = None) -> pd.DataFrame:
    path = path or KAGGLE_RAW
    if not path.exists():
        raise FileNotFoundError(f"Download Kaggle CSV to {path}. See docs/KAGGLE_SETUP.md.")
    return pd.read_csv(path)


def load_person_baselines(use_demo: bool = True) -> pd.DataFrame:
    if use_demo and BASELINES_DEMO.exists():
        return pd.read_csv(BASELINES_DEMO)
    df = load_feature_table(use_demo=use_demo)
    return compute_person_baselines(df)


def load_feature_table(use_demo: bool = False) -> pd.DataFrame:
    if not use_demo and DEFAULT_PROCESSED.exists():
        df = pd.read_csv(DEFAULT_PROCESSED)
    elif not use_demo and KAGGLE_RAW.exists():
        raw = load_kaggle_raw()
        df = build_features_from_kaggle(raw)
        df[LABEL_STRAIN] = strain_label(df)
    elif DEFAULT_DEMO.exists():
        df = pd.read_csv(DEFAULT_DEMO)
    else:
        raise FileNotFoundError("Run scripts/generate_demo_data.py or add Kaggle data.")

    if LABEL_STRAIN not in df.columns and "fatigue_high" in df.columns:
        df[LABEL_STRAIN] = df["fatigue_high"]
    if LABEL_STRAIN not in df.columns:
        raise ValueError(f"Missing {LABEL_STRAIN} column.")
    return df


def participant_groups(df: pd.DataFrame) -> pd.Series:
    if COL_PARTICIPANT in df.columns:
        return df[COL_PARTICIPANT].astype(str)
    return pd.Series(range(len(df)), index=df.index)
