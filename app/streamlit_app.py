"""
Streamlit demo — GDSC showcase (Sessions 7–8).

Run: streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_loader import load_feature_table
from src.models import FEATURE_COLUMNS, load_model, predict_fatigue

st.set_page_config(page_title="Fatigue Insight", page_icon="💤", layout="wide")

st.title("Wearable Fatigue Insight")
st.caption(
    "Educational prototype — not medical advice. "
    "Built from sleep & heart-rate features (PMData-style pipeline)."
)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Tonight's inputs")
    sleep_efficiency = st.slider("Sleep efficiency", 0.5, 0.99, 0.82, 0.01)
    rem_ratio = st.slider("REM ratio", 0.05, 0.35, 0.18, 0.01)
    deep_ratio = st.slider("Deep sleep ratio", 0.05, 0.35, 0.16, 0.01)
    resting_hr = st.slider("Resting heart rate (bpm)", 48, 90, 62)
    steps = st.slider("Steps yesterday", 500, 15000, 7500, 500)
    hr_elevated = st.slider("HR elevation vs baseline", 0.0, 15.0, 2.0, 0.5)

    row = {
        "sleep_efficiency": sleep_efficiency,
        "rem_ratio": rem_ratio,
        "deep_ratio": deep_ratio,
        "resting_hr": resting_hr,
        "steps": steps,
        "hr_elevated": hr_elevated,
    }

    if st.button("Predict fatigue risk", type="primary"):
        pipe = load_model()
        label, proba = predict_fatigue(row, pipe)
        st.session_state["last_proba"] = proba
        st.session_state["last_label"] = label

with col_right:
    st.subheader("Model output")
    proba = st.session_state.get("last_proba")
    if proba is None:
        st.info("Adjust sliders and click **Predict fatigue risk**.")
    else:
        st.progress(proba, text=f"Estimated high-fatigue probability: {proba:.0%}")
        if st.session_state["last_label"] == 1:
            st.warning("Signal suggests **elevated fatigue** — prioritize rest and recovery.")
        else:
            st.success("Signal is closer to **typical recovery** for this feature pattern.")

    with st.expander("Sample data from training table"):
        try:
            df = load_feature_table(use_demo=True)
            st.dataframe(df.head(20), use_container_width=True)
        except FileNotFoundError:
            st.write("Run `python scripts/generate_demo_data.py` to create sample data.")

st.divider()
st.markdown(
    """
**Presentation talking points**
- Features used: """
    + ", ".join(FEATURE_COLUMNS)
    + """
- Model: sklearn pipeline saved with joblib
- Limitations: rule-based labels, small demo set, no personalization
"""
)
