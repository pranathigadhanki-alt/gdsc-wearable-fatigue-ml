"""
Load the Kaggle feature table for modeling.

Session 1: `load_kaggle_raw`
Session 3: wire Kaggle → features → `load_feature_table`
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.kaggle_schema import KAGGLE_FILENAME, LABEL_FATIGUE

REPO_ROOT = Path(__file__).resolve().parents[1]
KAGGLE_RAW = REPO_ROOT / "data" / "kaggle" / KAGGLE_FILENAME
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
DEFAULT_PROCESSED = REPO_ROOT / "data" / "processed" / "features_v1.csv"


def load_kaggle_raw(path: Path | None = None) -> pd.DataFrame:
    """
    Session 1 — Read the Kaggle CSV from `data/kaggle/`.

    Steps:
      1. Set `path` to `KAGGLE_RAW` when None.
      2. Use pandas to read the CSV.
      3. Return the DataFrame.
    """
    # TODO: path = path or KAGGLE_RAW
    # TODO: if not path.exists(): raise FileNotFoundError with docs/KAGGLE_SETUP.md hint
    # TODO: return pd.read_csv(path)
    raise NotImplementedError("Complete load_kaggle_raw in Session 1 (see notebook).")


def load_feature_table(use_demo: bool = False) -> pd.DataFrame:
    """
    Return one row per person with numeric features and `fatigue_high` (0/1).

    Priority (Session 3):
      1. `data/processed/features_v1.csv` if it exists and use_demo is False
      2. Kaggle raw → call `build_features_from_kaggle` + `fatigue_label` from src.features
      3. `data/sample_demo.csv` for practice before Kaggle download
    """
    # TODO: implement priority chain above
    # TODO: ensure LABEL_FATIGUE column exists before returning
    if use_demo and DEFAULT_DEMO.exists():
        return pd.read_csv(DEFAULT_DEMO)
    raise NotImplementedError("Complete load_feature_table in Session 3.")


def participant_groups(df: pd.DataFrame) -> pd.Series:
    """
    Session 4 — Group key for train/test split (one row per person).

    Hint: use column `participant_id` when present.
    """
    # TODO: if "participant_id" in df.columns: return df["participant_id"].astype(str)
    # TODO: else return pd.Series(range(len(df)), index=df.index)
    raise NotImplementedError("Complete participant_groups in Session 4.")
