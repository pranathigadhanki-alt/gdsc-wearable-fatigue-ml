"""
Feature engineering — Kaggle Sleep Health and Lifestyle dataset.

Fill in each function during Sessions 2–3. Column names: see `src/kaggle_schema.py`.
"""

from __future__ import annotations

import pandas as pd

from src.kaggle_schema import (
    COL_ACTIVITY,
    COL_HEART_RATE,
    COL_HR,
    COL_PARTICIPANT,
    COL_PERSON_ID,
    COL_PHYSICAL_ACTIVITY,
    COL_QUALITY,
    COL_QUALITY_OF_SLEEP,
    COL_SLEEP_DURATION,
    COL_SLEEP_DURATION_H,
    COL_STRESS,
    COL_STRESS_LEVEL,
    COL_STEPS,
    COL_DAILY_STEPS,
)


def build_features_from_kaggle(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Session 3 — Rename Kaggle columns to snake_case and add helper features.

    Required renames (use DataFrame.rename):
      Person ID → participant_id
      Sleep Duration → sleep_duration
      Quality of Sleep → quality_of_sleep
      Physical Activity Level → physical_activity_level
      Stress Level → stress_level
      Heart Rate → heart_rate
      Daily Steps → daily_steps

    Then:
      - Cast age, heart_rate, daily_steps to numeric (errors='coerce').
      - Add `gender_male`: 1 if Gender is Male else 0.
      - Add `stress_x_poor_sleep`: stress_level * (10 - quality_of_sleep)
    """
    df = raw.copy()
    # TODO: df = df.rename(columns={ ... })
    # TODO: numeric casts
    # TODO: gender_male
    # TODO: stress_x_poor_sleep
    raise NotImplementedError("Complete build_features_from_kaggle in Session 3.")


def fatigue_label(df: pd.DataFrame) -> pd.Series:
    """
    Session 3 — Rule-based label (not medical ground truth).

    Default charter rule (change if your team agreed differently):
      fatigue_high = 1 when stress_level >= 7 OR quality_of_sleep <= 5
    """
    # TODO: build boolean Series `high`, return high.astype(int)
    raise NotImplementedError("Complete fatigue_label in Session 3.")
