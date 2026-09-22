"""Sessions 5–7 — predict strain from watch signals + baseline deltas only."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = REPO_ROOT / "models" / "strain_classifier.joblib"

FEATURE_COLUMNS = [
    "sleep_duration",
    "heart_rate",
    "daily_steps",
    "physical_activity_level",
    "sleep_duration_delta",
    "heart_rate_delta",
    "daily_steps_delta",
    "physical_activity_level_delta",
]


def build_logistic_pipeline() -> Pipeline:
    raise NotImplementedError("Session 5")


def build_rf_pipeline() -> Pipeline:
    raise NotImplementedError("Session 5")


def train_model(use_demo: bool = True) -> Pipeline:
    raise NotImplementedError("Session 7")


def save_model(pipe: Pipeline, path: Path | None = None) -> Path:
    path = path or MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, path)
    return path


def load_model(path: Path | None = None) -> Pipeline:
    path = path or MODEL_PATH
    if not path.exists():
        pipe = train_model(use_demo=True)
        save_model(pipe, path)
    return joblib.load(path)


def predict_strain(row: pd.Series | dict, pipe: Pipeline | None = None) -> tuple[int, float]:
    raise NotImplementedError("Session 7")


predict_fatigue = predict_strain  # notebook alias
