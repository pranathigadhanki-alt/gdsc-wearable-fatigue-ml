"""Mentor reference — sklearn pipelines."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from solutions.data_loader import load_feature_table, participant_groups

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = REPO_ROOT / "models" / "fatigue_classifier.joblib"

FEATURE_COLUMNS = [
    "sleep_duration",
    "quality_of_sleep",
    "physical_activity_level",
    "heart_rate",
    "daily_steps",
    "age",
    "stress_x_poor_sleep",
]


def build_logistic_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )


def build_rf_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=200, class_weight="balanced", random_state=42
                ),
            ),
        ]
    )


def train_model(use_demo: bool = True) -> Pipeline:
    df = load_feature_table(use_demo=use_demo)
    X = df[FEATURE_COLUMNS]
    y = df["fatigue_high"]
    groups = participant_groups(df)
    split = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, _ = next(split.split(X, y, groups=groups))
    pipe = build_rf_pipeline()
    pipe.fit(X.iloc[train_idx], y.iloc[train_idx])
    return pipe


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


def predict_fatigue(row: pd.Series | dict, pipe: Pipeline | None = None) -> tuple[int, float]:
    pipe = pipe or load_model()
    if isinstance(row, dict):
        row = pd.Series(row)
    X = row[FEATURE_COLUMNS].to_frame().T
    proba = float(pipe.predict_proba(X)[0, 1])
    return int(proba >= 0.5), proba
