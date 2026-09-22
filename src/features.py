"""Session 3 — Kaggle → watch features + baseline deltas. Labels hidden from UI."""

from __future__ import annotations

import pandas as pd


def build_features_from_kaggle(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Rename Kaggle columns, then call:
      - compute_person_baselines
      - add_baseline_deltas
    See solutions/features.py and docs/BUILD_PATH.md Session 3.
    """
    raise NotImplementedError("Session 3: build_features_from_kaggle")


def strain_label(df: pd.DataFrame) -> pd.Series:
    """
    Training label only (stress ≥ 7 OR sleep quality ≤ 5).
    The app never asks the user these questions at inference time.
    """
    raise NotImplementedError("Session 3: strain_label")
