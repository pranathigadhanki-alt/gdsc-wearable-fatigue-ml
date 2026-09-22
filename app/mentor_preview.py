from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.dashboard import run_dashboard
from solutions.counterfactuals import suggest_what_ifs
from solutions.data_loader import load_feature_table, load_person_baselines
from solutions.explain import explain_prediction
from solutions.models import FEATURE_COLUMNS, predict_recovery, save_model, train_model

run_dashboard(
    load_feature_table=load_feature_table,
    load_person_baselines=load_person_baselines,
    feature_columns=FEATURE_COLUMNS,
    train_model=train_model,
    save_model=save_model,
    predict_recovery=predict_recovery,
    explain_prediction=explain_prediction,
    suggest_what_ifs=suggest_what_ifs,
    subtitle=(
        "People with insomnia or sleep apnea in public data. Watch signals + your baseline + last night → "
        "chance of a **better night tomorrow**, plus what to try — not replacing a sleep study or doctor."
    ),
)
