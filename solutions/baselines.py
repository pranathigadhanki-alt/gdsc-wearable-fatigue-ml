"""Personal baselines + disorder profile."""

from __future__ import annotations

import pandas as pd

from src.kaggle_schema import COL_DISORDER, COL_PARTICIPANT, WATCH_SIGNALS


def compute_person_baselines(df: pd.DataFrame) -> pd.DataFrame:
    base = df.groupby(COL_PARTICIPANT, as_index=False)[list(WATCH_SIGNALS)].median()
    if COL_DISORDER in df.columns:
        d = df.groupby(COL_PARTICIPANT)[COL_DISORDER].first().reset_index()
        base = base.merge(d, on=COL_PARTICIPANT)
    return base


def add_baseline_deltas(df: pd.DataFrame, baselines: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    base_map = baselines.set_index(COL_PARTICIPANT)
    for col in WATCH_SIGNALS:
        out[f"{col}_delta"] = out[col] - out[COL_PARTICIPANT].map(base_map[col])
    return out


def build_model_row(participant_id, today: dict, last_night: dict, baselines: pd.DataFrame) -> dict:
    match = baselines[baselines[COL_PARTICIPANT] == participant_id]
    if match.empty:
        match = baselines.iloc[[0]]
    b = match.iloc[0]
    row: dict = {}
    for col in WATCH_SIGNALS:
        row[col] = float(today[col])
        row[f"lag1_{col}"] = float(last_night[col])
        row[f"{col}_delta"] = row[col] - float(b[col])
    disorder = str(b.get(COL_DISORDER, "Insomnia"))
    row["disorder_insomnia"] = int(disorder == "Insomnia")
    row["disorder_apnea"] = int(disorder == "Sleep Apnea")
    return row


watch_row_with_deltas = build_model_row
