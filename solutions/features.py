"""Features: watch signals + personal baseline deltas. Labels from hidden self-report."""

from __future__ import annotations

import pandas as pd

from solutions.baselines import add_baseline_deltas, compute_person_baselines
from src.kaggle_schema import (
    COL_ACTIVITY,
    COL_AGE_SNAKE,
    COL_GENDER,
    COL_HEART_RATE,
    COL_HR,
    COL_PARTICIPANT,
    COL_PERSON_ID,
    COL_PHYSICAL_ACTIVITY,
    COL_QUALITY,
    COL_QUALITY_OF_SLEEP,
    COL_SLEEP_DURATION,
    COL_SLEEP_DURATION_H,
    COL_STEPS,
    COL_DAILY_STEPS,
    COL_STRESS,
    COL_STRESS_LEVEL,
    LABEL_STRAIN,
)


def build_features_from_kaggle(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    rename = {
        COL_PERSON_ID: COL_PARTICIPANT,
        COL_SLEEP_DURATION: COL_SLEEP_DURATION_H,
        COL_QUALITY_OF_SLEEP: COL_QUALITY,
        COL_PHYSICAL_ACTIVITY: COL_ACTIVITY,
        COL_STRESS_LEVEL: COL_STRESS,
        COL_HEART_RATE: COL_HR,
        COL_DAILY_STEPS: COL_STEPS,
        "Age": COL_AGE_SNAKE,
    }
    df = df.rename(columns=rename)
    df[COL_AGE_SNAKE] = pd.to_numeric(df[COL_AGE_SNAKE], errors="coerce")
    for c in (COL_HR, COL_STEPS, COL_SLEEP_DURATION_H, COL_ACTIVITY):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["gender_male"] = (df[COL_GENDER].str.lower() == "male").astype(int)

    baselines = compute_person_baselines(df)
    df = add_baseline_deltas(df, baselines)
    return df


def strain_label(df: pd.DataFrame) -> pd.Series:
    """
    Training-only label (not asked in the demo UI).
    Ground truth from Kaggle self-report — model learns to predict this from watch signals + deltas.
    """
    high_stress = df[COL_STRESS] >= 7
    poor_sleep = df[COL_QUALITY] <= 5
    return (high_stress | poor_sleep).astype(int)
