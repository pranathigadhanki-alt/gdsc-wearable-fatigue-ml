"""Session 3 — lags, disorder cohort, better_night_tomorrow label."""

from __future__ import annotations

import pandas as pd


def build_features_from_kaggle(raw: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Session 3 — see solutions/features.py")


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Session 3")


def better_night_tomorrow_label(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("Session 3")


def filter_disorder_cohort(df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Session 3")


def prepare_training_frame(df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Session 3")
