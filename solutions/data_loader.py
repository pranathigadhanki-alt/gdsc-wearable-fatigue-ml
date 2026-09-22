"""Feature table — disorder cohort, lags, recovery label."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from solutions.baselines import compute_person_baselines
from solutions.features import build_features_from_kaggle, prepare_training_frame
from src.kaggle_schema import COL_DISORDER, COL_PARTICIPANT, KAGGLE_FILENAME, LABEL_RECOVERY

REPO_ROOT = Path(__file__).resolve().parents[1]
KAGGLE_RAW = REPO_ROOT / "data" / "kaggle" / KAGGLE_FILENAME
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
BASELINES_DEMO = REPO_ROOT / "data" / "person_baselines.csv"


def load_kaggle_raw(path: Path | None = None) -> pd.DataFrame:
    path = path or KAGGLE_RAW
    if not path.exists():
        raise FileNotFoundError(f"Download Kaggle CSV to {path}. See docs/KAGGLE_SETUP.md.")
    return pd.read_csv(path)


def load_feature_table(use_demo: bool = True) -> pd.DataFrame:
    if not use_demo and KAGGLE_RAW.exists():
        raw = load_kaggle_raw()
        df = build_features_from_kaggle(raw)
        return prepare_training_frame(df)
    if DEFAULT_DEMO.exists():
        return pd.read_csv(DEFAULT_DEMO)
    raise FileNotFoundError("Run scripts/generate_demo_data.py")


def load_person_baselines(use_demo: bool = True) -> pd.DataFrame:
    if use_demo and BASELINES_DEMO.exists():
        base = pd.read_csv(BASELINES_DEMO)
        if COL_DISORDER not in base.columns:
            df = load_feature_table(use_demo=True)
            disorder = df.groupby(COL_PARTICIPANT)[COL_DISORDER].first().reset_index()
            base = base.merge(disorder, on=COL_PARTICIPANT, how="left")
        return base
    df = load_feature_table(use_demo=use_demo)
    base = compute_person_baselines(df)
    if COL_DISORDER in df.columns:
        disorder = df.groupby(COL_PARTICIPANT)[COL_DISORDER].first().reset_index()
        base = base.merge(disorder, on=COL_PARTICIPANT)
    return base


def participant_groups(df: pd.DataFrame) -> pd.Series:
    return df[COL_PARTICIPANT].astype(str)
