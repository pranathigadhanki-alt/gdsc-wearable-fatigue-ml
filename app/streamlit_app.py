"""
Streamlit demo — Sessions 7–8 (after `src/models.py` is complete).

Run: streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO Session 7: uncomment when predict_fatigue works
# from src.data_loader import load_feature_table
# from src.models import FEATURE_COLUMNS, load_model, predict_fatigue

st.set_page_config(page_title="Fatigue Insight", page_icon="💤", layout="wide")

st.title("Wearable Fatigue Insight")
st.caption(
    "GDSC learning project — Kaggle Sleep Health & Lifestyle features. Not medical advice."
)

st.info(
    "Finish **`src/models.py`** (Session 7), then uncomment the imports at the top of this file."
)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Inputs (match your FEATURE_COLUMNS)")
    sleep_duration = st.slider("Sleep duration (hours)", 5.0, 9.0, 7.0, 0.1)
    quality_of_sleep = st.slider("Quality of sleep (1–10)", 1, 10, 6)
    physical_activity = st.slider("Physical activity (min/day)", 0, 100, 45)
    heart_rate = st.slider("Heart rate (bpm)", 55, 95, 72)
    daily_steps = st.slider("Daily steps", 1000, 15000, 6000, 500)
    age = st.slider("Age", 20, 65, 30)
    stress_x_poor_sleep = st.slider("stress × (10 − quality)", 0, 80, 24)

    row = {
        "sleep_duration": sleep_duration,
        "quality_of_sleep": quality_of_sleep,
        "physical_activity_level": physical_activity,
        "heart_rate": heart_rate,
        "daily_steps": daily_steps,
        "age": age,
        "stress_x_poor_sleep": stress_x_poor_sleep,
    }

    if st.button("Predict fatigue risk", type="primary"):
        # TODO Session 7: pipe = load_model(); label, proba = predict_fatigue(row, pipe)
        st.session_state["msg"] = "Wire up predict_fatigue in src/models.py first."

with col_right:
    st.subheader("Model output")
    st.write(st.session_state.get("msg", "Click predict after Session 7 code is ready."))

    # TODO Session 7: show st.progress(proba), warning/success by label
    # TODO Session 7: st.dataframe(load_feature_table(use_demo=True).head())

st.divider()
st.markdown(
    """
**Showcase talking points**
- Data: [Kaggle Sleep Health and Lifestyle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)
- Label: team rule in `templates/team_charter.md`
- Model: sklearn pipeline + joblib
"""
)
