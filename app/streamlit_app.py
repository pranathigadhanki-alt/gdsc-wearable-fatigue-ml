"""
Mentee app — same UI as mentor preview when `src/` is complete (Sessions 1–7).

Run: PYTHONPATH=. streamlit run app/streamlit_app.py
Progress: python scripts/check_session.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui_theme import hero, inject_theme
from app.progress import ready_for_dashboard, session_status

st.set_page_config(page_title="Fatigue Insight", page_icon="💤", layout="wide")

if not ready_for_dashboard():
    inject_theme()
    hero("Stress & Fatigue Insight", "Build week by week — your app matches the mentor preview when Session 7 is done.")
    st.markdown("### Your progress")
    for line in session_status():
        st.markdown(line)
    st.markdown(
        """
Follow **[docs/BUILD_PATH.md](../docs/BUILD_PATH.md)** and the notebook for each session.

When all Session 7 checks pass, restart this app to load the full dashboard.
"""
    )
    st.stop()

from app.dashboard import run_dashboard
from src.data_loader import load_feature_table
from src.explain import explain_prediction
from src.models import FEATURE_COLUMNS, predict_fatigue, save_model, train_model

run_dashboard(
    load_feature_table=load_feature_table,
    feature_columns=FEATURE_COLUMNS,
    train_model=train_model,
    save_model=save_model,
    predict_fatigue=predict_fatigue,
    explain_prediction=explain_prediction,
    subtitle="Built by your team — same experience as the GDSC demo.",
)
