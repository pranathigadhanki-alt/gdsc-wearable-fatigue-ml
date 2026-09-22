"""Mentor shortcut — same UI as mentees build; uses `solutions/`."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.dashboard import run_dashboard
from solutions.data_loader import load_feature_table
from solutions.explain import explain_prediction
from solutions.models import FEATURE_COLUMNS, predict_fatigue, save_model, train_model

run_dashboard(
    load_feature_table=load_feature_table,
    feature_columns=FEATURE_COLUMNS,
    train_model=train_model,
    save_model=save_model,
    predict_fatigue=predict_fatigue,
    explain_prediction=explain_prediction,
    subtitle="Mentor preview (`solutions/`) — mentees reach this via `src/` + `streamlit_app.py`.",
)
