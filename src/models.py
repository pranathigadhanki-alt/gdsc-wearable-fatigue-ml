"""
Train and load sklearn pipelines — Sessions 5–7.

Complete each function before running Streamlit with your trained model.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = REPO_ROOT / "models" / "fatigue_classifier.joblib"

# Session 3 — verify these match your feature table after engineering
FEATURE_COLUMNS = [
    "sleep_duration",
    "quality_of_sleep",
    "physical_activity_level",
    "heart_rate",
    "daily_steps",
    "age",
    "stress_x_poor_sleep",  # Session 3 — must exist in your feature table
]


def build_logistic_pipeline() -> Pipeline:
    """Session 5 — StandardScaler + LogisticRegression(class_weight='balanced')."""
    # TODO: return Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(...))])
    raise NotImplementedError("Complete build_logistic_pipeline in Session 5.")


def build_rf_pipeline() -> Pipeline:
    """Session 5 — RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)."""
    # TODO: return Pipeline([("clf", RandomForestClassifier(...))])
    raise NotImplementedError("Complete build_rf_pipeline in Session 5.")


def train_model(use_demo: bool = True) -> Pipeline:
    """Session 7 — Fit your chosen pipeline on a group split (see notebook)."""
    # TODO: from src.data_loader import load_feature_table, participant_groups
    # TODO: load X, y; GroupShuffleSplit; fit pipeline on train_idx
    raise NotImplementedError("Complete train_model in Session 7.")


def save_model(pipe: Pipeline, path: Path | None = None) -> Path:
    """Session 7 — joblib.dump to models/fatigue_classifier.joblib"""
    path = path or MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, path)
    return path


def load_model(path: Path | None = None) -> Pipeline:
    """Session 7 — Load saved pipeline or train demo model if missing."""
    path = path or MODEL_PATH
    if not path.exists():
        pipe = train_model(use_demo=True)
        save_model(pipe, path)
    return joblib.load(path)


def predict_fatigue(row: pd.Series | dict, pipe: Pipeline | None = None) -> tuple[int, float]:
    """Session 7 — Return (label, probability of fatigue_high)."""
    pipe = pipe or load_model()
    if isinstance(row, dict):
        row = pd.Series(row)
    # TODO: X = row[FEATURE_COLUMNS].to_frame().T
    # TODO: proba = pipe.predict_proba(X)[0, 1]; return int(proba >= 0.5), float(proba)
    raise NotImplementedError("Complete predict_fatigue in Session 7.")
