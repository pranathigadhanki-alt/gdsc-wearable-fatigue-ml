"""Session 1 & 3 — Kaggle + feature table + baselines."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.kaggle_schema import KAGGLE_FILENAME

REPO_ROOT = Path(__file__).resolve().parents[1]
KAGGLE_RAW = REPO_ROOT / "data" / "kaggle" / KAGGLE_FILENAME
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
BASELINES_DEMO = REPO_ROOT / "data" / "person_baselines.csv"


def load_kaggle_raw(path: Path | None = None) -> pd.DataFrame:
    raise NotImplementedError("Session 1: load_kaggle_raw")


def load_feature_table(use_demo: bool = False) -> pd.DataFrame:
    if use_demo and DEFAULT_DEMO.exists():
        return pd.read_csv(DEFAULT_DEMO)
    raise NotImplementedError("Session 3: load_feature_table")


def load_person_baselines(use_demo: bool = True) -> pd.DataFrame:
    if use_demo and BASELINES_DEMO.exists():
        return pd.read_csv(BASELINES_DEMO)
    raise NotImplementedError("Session 3: load_person_baselines")


def participant_groups(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("Session 4: participant_groups")
