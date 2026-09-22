"""Feature engineering helpers (extend each week in class)."""

from __future__ import annotations

import pandas as pd


def nightly_sleep_features(raw_nights: pd.DataFrame) -> pd.DataFrame:
    """
    Build one row per night from raw sleep summaries.

    Expected columns (adapt to PMData names in Week 3):
    participant_id, date, time_in_bed_min, sleep_min, rem_min, deep_min,
    awake_min, resting_hr, steps
    """
    required = {"participant_id", "date", "sleep_min", "time_in_bed_min", "resting_hr"}
    missing = required - set(raw_nights.columns)
    if missing:
        raise ValueError(f"Missing columns for nightly features: {sorted(missing)}")

    df = raw_nights.copy()
    df["sleep_efficiency"] = df["sleep_min"] / df["time_in_bed_min"].clip(lower=1)
    if "rem_min" in df.columns and "deep_min" in df.columns:
        total = df["sleep_min"].clip(lower=1)
        df["rem_ratio"] = df["rem_min"] / total
        df["deep_ratio"] = df["deep_min"] / total
    else:
        df["rem_ratio"] = 0.0
        df["deep_ratio"] = 0.0

    df["steps"] = df.get("steps", 0)
    df["hr_elevated"] = (df["resting_hr"] - df["resting_hr"].median()).clip(lower=0)

    return df


def rule_based_fatigue_label(df: pd.DataFrame) -> pd.Series:
    """
    Educational label: NOT clinical ground truth.

    High fatigue if sleep efficiency is low OR resting HR is high vs cohort.
    """
    eff_thr = df["sleep_efficiency"].quantile(0.25)
    hr_thr = df["resting_hr"].quantile(0.75)
    high = (df["sleep_efficiency"] <= eff_thr) | (df["resting_hr"] >= hr_thr)
    return high.astype(int)
