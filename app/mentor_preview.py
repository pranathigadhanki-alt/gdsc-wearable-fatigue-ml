"""Mentor preview — full StrainScope using `solutions/`."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.dashboard import run_dashboard
from solutions.counterfactuals import suggest_what_ifs
from solutions.data_loader import load_feature_table, load_person_baselines
from solutions.explain import explain_prediction
from solutions.models import FEATURE_COLUMNS, predict_strain, save_model, train_model

run_dashboard(
    load_feature_table=load_feature_table,
    load_person_baselines=load_person_baselines,
    feature_columns=FEATURE_COLUMNS,
    train_model=train_model,
    save_model=save_model,
    predict_strain=predict_strain,
    explain_prediction=explain_prediction,
    suggest_what_ifs=suggest_what_ifs,
    subtitle=(
        "We don’t ask how stressed you feel. Watch-like signals + *your* baseline → "
        "next-day strain estimate, with what-if scenarios."
    ),
)
