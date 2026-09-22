"""Load demo or processed feature tables for modeling."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEMO = REPO_ROOT / "data" / "sample_demo.csv"
DEFAULT_PROCESSED = REPO_ROOT / "data" / "processed" / "features_v1.csv"


def load_feature_table(use_demo: bool = False) -> pd.DataFrame:
    """
    Return a nightly feature table with column `fatigue_high` (0/1).

    Students replace demo mode with PMData-derived CSV from Week 3 onward.
    """
    path = DEFAULT_DEMO if use_demo or not DEFAULT_PROCESSED.exists() else DEFAULT_PROCESSED
    if not path.exists():
        raise FileNotFoundError(
            f"No data at {path}. Run scripts/generate_demo_data.py or build features_v1.csv."
        )
    df = pd.read_csv(path)
    if "fatigue_high" not in df.columns:
        raise ValueError("Expected label column `fatigue_high` in feature table.")
    return df


def participant_day_groups(df: pd.DataFrame) -> pd.Series:
    """Group key for split — one row per participant-day."""
    if "participant_id" in df.columns and "date" in df.columns:
        return df["participant_id"].astype(str) + "_" + df["date"].astype(str)
    return pd.Series(range(len(df)), index=df.index)
