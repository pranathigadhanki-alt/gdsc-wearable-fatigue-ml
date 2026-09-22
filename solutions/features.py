"""Watch signals, baselines, lags, disorder cohort — label = better night tomorrow."""

from __future__ import annotations

import pandas as pd

from solutions.baselines import add_baseline_deltas, compute_person_baselines
from src.kaggle_schema import (
    COL_ACTIVITY,
    COL_AGE_SNAKE,
    COL_DISORDER,
    COL_GENDER,
    COL_HEART_RATE,
    COL_HR,
    COL_PARTICIPANT,
    COL_PERSON_ID,
    COL_PHYSICAL_ACTIVITY,
    COL_QUALITY,
    COL_QUALITY_OF_SLEEP,
    COL_SLEEP_DISORDER,
    COL_SLEEP_DURATION,
    COL_SLEEP_DURATION_H,
    COL_STEPS,
    COL_DAILY_STEPS,
    DISORDER_COHORT,
    LABEL_RECOVERY,
    WATCH_SIGNALS,
)


def build_features_from_kaggle(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    rename = {
        COL_PERSON_ID: COL_PARTICIPANT,
        COL_SLEEP_DURATION: COL_SLEEP_DURATION_H,
        COL_QUALITY_OF_SLEEP: COL_QUALITY,
        COL_PHYSICAL_ACTIVITY: COL_ACTIVITY,
        COL_HEART_RATE: COL_HR,
        COL_DAILY_STEPS: COL_STEPS,
        "Age": COL_AGE_SNAKE,
        COL_SLEEP_DISORDER: COL_DISORDER,
    }
    df = df.rename(columns=rename)
    df[COL_AGE_SNAKE] = pd.to_numeric(df[COL_AGE_SNAKE], errors="coerce")
    for c in (COL_HR, COL_STEPS, COL_SLEEP_DURATION_H, COL_ACTIVITY, COL_QUALITY):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["gender_male"] = (df[COL_GENDER].str.lower() == "male").astype(int)
    df["disorder_insomnia"] = (df[COL_DISORDER] == "Insomnia").astype(int)
    df["disorder_apnea"] = (df[COL_DISORDER] == "Sleep Apnea").astype(int)

    baselines = compute_person_baselines(df)
    df = add_baseline_deltas(df, baselines)
    df = add_lag_features(df)
    return df


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values([COL_PARTICIPANT]).reset_index(drop=True)
    for col in WATCH_SIGNALS:
        df[f"lag1_{col}"] = df.groupby(COL_PARTICIPANT)[col].shift(1)
    return df


def better_night_tomorrow_label(df: pd.DataFrame) -> pd.Series:
    """
    Training-only: tomorrow's sleep quality rises OR sleep duration increases meaningfully.
    Not shown in the demo UI — model learns from history in public data.
    """
    next_q = df.groupby(COL_PARTICIPANT)[COL_QUALITY].shift(-1)
    next_sleep = df.groupby(COL_PARTICIPANT)[COL_SLEEP_DURATION_H].shift(-1)
    better = (next_q > df[COL_QUALITY]) | (next_sleep >= df[COL_SLEEP_DURATION_H] + 0.25)
    return better


def filter_disorder_cohort(df: pd.DataFrame) -> pd.DataFrame:
    """Focus on insomnia & sleep apnea rows (project narrative)."""
    return df[df[COL_DISORDER].isin(DISORDER_COHORT)].copy()


def prepare_training_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows without lag or without tomorrow label."""
    out = filter_disorder_cohort(df)
    out[LABEL_RECOVERY] = better_night_tomorrow_label(out)
    out = out[out[LABEL_RECOVERY].notna() & out["lag1_sleep_duration"].notna()].copy()
    out[LABEL_RECOVERY] = out[LABEL_RECOVERY].astype(int)
    return out
