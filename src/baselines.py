"""Session 3 — Personal baselines (see `solutions/baselines.py`)."""

from __future__ import annotations

import pandas as pd

from src.kaggle_schema import COL_PARTICIPANT, WATCH_SIGNALS


def compute_person_baselines(df: pd.DataFrame) -> pd.DataFrame:
    # TODO Session 3: groupby participant_id, median of WATCH_SIGNALS
    raise NotImplementedError("Session 3: compute_person_baselines")


def add_baseline_deltas(df: pd.DataFrame, baselines: pd.DataFrame) -> pd.DataFrame:
    # TODO Session 3: for each WATCH_SIGNALS col, add f"{col}_delta"
    raise NotImplementedError("Session 3: add_baseline_deltas")


def build_model_row(
    participant_id,
    today: dict,
    last_night: dict,
    baselines: pd.DataFrame,
) -> dict:
    # TODO Session 7: tonight + lag1 + deltas + disorder flags
    raise NotImplementedError("Session 7: build_model_row")


watch_row_with_deltas = build_model_row  # legacy name
