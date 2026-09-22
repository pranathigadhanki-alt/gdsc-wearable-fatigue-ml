"""Mentor reference — feature engineering for Kaggle sleep / lifestyle data."""

from __future__ import annotations

import pandas as pd

from src.kaggle_schema import (
    COL_ACTIVITY,
    COL_AGE,
    COL_AGE_SNAKE,
    COL_DAILY_STEPS,
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
    COL_STRESS,
    COL_STRESS_LEVEL,
    LABEL_FATIGUE,
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
    df[COL_HR] = pd.to_numeric(df[COL_HR], errors="coerce")
    df[COL_STEPS] = pd.to_numeric(df[COL_STEPS], errors="coerce")
    df["gender_male"] = (df[COL_GENDER].str.lower() == "male").astype(int)
    df["stress_x_poor_sleep"] = df[COL_STRESS] * (10 - df[COL_QUALITY])
    return df


def fatigue_label(df: pd.DataFrame) -> pd.Series:
    """High fatigue proxy: high stress OR low sleep quality (club charter default)."""
    high_stress = df[COL_STRESS] >= 7
    poor_sleep = df[COL_QUALITY] <= 5
    return (high_stress | poor_sleep).astype(int)
