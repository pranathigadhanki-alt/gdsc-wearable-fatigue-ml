"""
Streamlit demo — Sessions 7–8 (after `src/models.py` + `src/explain.py` are complete).

Mentor preview (full UI): PYTHONPATH=. streamlit run app/mentor_preview.py

Run: streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui_theme import hero, inject_theme

st.set_page_config(page_title="Fatigue Insight", page_icon="💤", layout="wide")
inject_theme()

# TODO Session 7: uncomment when ready
# from src.data_loader import load_feature_table
# from src.explain import explain_prediction
# from src.models import FEATURE_COLUMNS, load_model, predict_fatigue

hero(
    "Stress & Fatigue Insight",
    "Student build — wire up `src/models.py` and `src/explain.py`, then copy patterns from `app/mentor_preview.py`.",
)

st.warning(
    "**Work in progress.** For the full colorful demo with explanations, mentors run: "
    "`PYTHONPATH=. streamlit run app/mentor_preview.py`"
)

st.markdown(
    """
### Session 7 checklist
1. Implement `predict_fatigue` in `src/models.py`
2. Implement `explain_prediction` in `src/explain.py` (see `solutions/explain.py`)
3. Reuse `app/ui_theme.py` and tabs from `app/mentor_preview.py`
"""
)
