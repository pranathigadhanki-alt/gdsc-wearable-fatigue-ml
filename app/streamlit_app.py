from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.progress import ready_for_dashboard, session_status
from app.ui_theme import hero, inject_theme

st.set_page_config(page_title="RecoveryScope", page_icon="🌙", layout="wide")

if not ready_for_dashboard():
    inject_theme()
    hero("RecoveryScope", "Build week by week → same app as mentor preview.")
    for line in session_status():
        st.markdown(line)
    st.info("[docs/BUILD_PATH.md](docs/BUILD_PATH.md) · Mentor: `app/mentor_preview.py`")
    st.stop()

from app.dashboard import run_dashboard
from src.counterfactuals import suggest_what_ifs
from src.data_loader import load_feature_table, load_person_baselines
from src.explain import explain_prediction
from src.models import FEATURE_COLUMNS, predict_recovery, save_model, train_model

run_dashboard(
    load_feature_table=load_feature_table,
    load_person_baselines=load_person_baselines,
    feature_columns=FEATURE_COLUMNS,
    train_model=train_model,
    save_model=save_model,
    predict_recovery=predict_recovery,
    explain_prediction=explain_prediction,
    suggest_what_ifs=suggest_what_ifs,
    subtitle="Built by your team — recovery-focused, disorder cohort.",
)
