"""Personal baselines — core of the «vs you» story."""

from __future__ import annotations

import pandas as pd

from src.kaggle_schema import COL_PARTICIPANT, WATCH_SIGNALS

BASELINE_SIGNALS = WATCH_SIGNALS


def compute_person_baselines(df: pd.DataFrame) -> pd.DataFrame:
    if COL_PARTICIPANT not in df.columns:
        raise ValueError(f"Need {COL_PARTICIPANT} for personal baselines.")
    return df.groupby(COL_PARTICIPANT, as_index=False)[list(BASELINE_SIGNALS)].median()


def add_baseline_deltas(df: pd.DataFrame, baselines: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    base_map = baselines.set_index(COL_PARTICIPANT)
    for col in BASELINE_SIGNALS:
        out[f"{col}_delta"] = out[col] - out[COL_PARTICIPANT].map(base_map[col])
    return out


def watch_row_with_deltas(participant_id, today: dict, baselines: pd.DataFrame) -> dict:
    match = baselines[baselines[COL_PARTICIPANT] == participant_id]
    if match.empty:
        match = baselines.iloc[[0]]
    b = match.iloc[0]
    out = {k: float(today[k]) for k in BASELINE_SIGNALS}
    for col in BASELINE_SIGNALS:
        out[f"{col}_delta"] = out[col] - float(b[col])
    return out
