"""
Mentor preview — full pipeline using `solutions/` (not student `src/`).

Run: PYTHONPATH=. streamlit run app/mentor_preview.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui_theme import hero, inject_theme, reason_card
from solutions.data_loader import load_feature_table
from solutions.explain import explain_prediction
from solutions.models import FEATURE_COLUMNS, predict_fatigue, train_model, save_model

st.set_page_config(
    page_title="Fatigue Insight",
    page_icon="💤",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

PRESETS = {
    "Custom (sliders)": None,
    "📚 Crunch week": {
        "sleep_duration": 5.8,
        "quality_of_sleep": 4,
        "physical_activity_level": 25,
        "heart_rate": 82,
        "daily_steps": 3500,
        "age": 22,
        "stress_x_poor_sleep": 48,
    },
    "😴 Recovery day": {
        "sleep_duration": 8.0,
        "quality_of_sleep": 9,
        "physical_activity_level": 55,
        "heart_rate": 64,
        "daily_steps": 9000,
        "age": 22,
        "stress_x_poor_sleep": 8,
    },
    "🏃 Active, short sleep": {
        "sleep_duration": 6.0,
        "quality_of_sleep": 6,
        "physical_activity_level": 85,
        "heart_rate": 78,
        "daily_steps": 12000,
        "age": 28,
        "stress_x_poor_sleep": 28,
    },
}


@st.cache_resource
def get_model_and_data():
    df = load_feature_table(use_demo=True)
    pipe = train_model(use_demo=True)
    save_model(pipe)
    return pipe, df


pipe, df = get_model_and_data()
defaults = df[FEATURE_COLUMNS].median()

with st.sidebar:
    st.markdown("### 🎛️ Quick scenarios")
    preset_name = st.selectbox("Load a profile", list(PRESETS.keys()))
    st.markdown("---")
    st.markdown("**About**")
    st.caption(
        "Educational demo — Kaggle Sleep Health & Lifestyle patterns. "
        "Not medical advice."
    )
    st.metric("Demo rows", len(df))
    st.metric("High fatigue %", f"{df['fatigue_high'].mean():.0%}")

hero(
    "Stress & Fatigue Insight",
    "See how sleep, stress, and heart rate combine — with a plain-language explanation.",
)

if "row" not in st.session_state:
    st.session_state.row = {c: float(defaults[c]) for c in FEATURE_COLUMNS}

if PRESETS[preset_name] is not None:
    st.session_state.row = dict(PRESETS[preset_name])
    st.session_state.pop("last_proba", None)

tab_input, tab_why, tab_data = st.tabs(["✨ Your day", "💬 Why this score?", "📊 Cohort data"])

with tab_input:
    left, mid, right = st.columns([1.1, 1, 1])

    with left:
        st.markdown("#### Adjust your signals")
        row = st.session_state.row
        row["sleep_duration"] = st.slider(
            "🌙 Sleep duration (hours)", 5.0, 9.0, float(row.get("sleep_duration", defaults["sleep_duration"])), 0.1
        )
        row["quality_of_sleep"] = st.slider(
            "✨ Sleep quality (1–10)", 1, 10, int(row.get("quality_of_sleep", defaults["quality_of_sleep"]))
        )
        row["stress_x_poor_sleep"] = st.slider(
            "⚡ Stress × poor sleep", 0, 80, int(row.get("stress_x_poor_sleep", defaults["stress_x_poor_sleep"]))
        )
        row["heart_rate"] = st.slider(
            "❤️ Heart rate (bpm)", 55, 95, int(row.get("heart_rate", defaults["heart_rate"]))
        )

    with mid:
        row["physical_activity_level"] = st.slider(
            "🏃 Activity (min/day)", 0, 100, int(row.get("physical_activity_level", defaults["physical_activity_level"]))
        )
        row["daily_steps"] = st.slider(
            "🚶 Daily steps", 1000, 15000, int(row.get("daily_steps", defaults["daily_steps"])), 500
        )
        row["age"] = st.slider("🎂 Age", 18, 70, int(row.get("age", defaults["age"])))
        st.session_state.row = row

        run = st.button("🔮 Update prediction", type="primary", use_container_width=True)

    with right:
        if run or "last_proba" not in st.session_state:
            label, proba = predict_fatigue(row, pipe)
            reasons, summary = explain_prediction(row, df, pipe, label, proba)
            st.session_state.update(
                last_proba=proba,
                last_label=label,
                last_summary=summary,
                last_reasons=reasons,
            )

        proba = st.session_state.get("last_proba", 0.0)
        label = st.session_state.get("last_label", 0)

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=proba * 100,
                number={"suffix": "%", "font": {"size": 40, "color": "#f8fafc"}},
                title={"text": "Fatigue risk", "font": {"color": "#e2e8f0"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                    "bar": {"color": "#a855f7" if label else "#14b8a6"},
                    "steps": [
                        {"range": [0, 40], "color": "rgba(34,197,94,0.35)"},
                        {"range": [40, 70], "color": "rgba(234,179,8,0.35)"},
                        {"range": [70, 100], "color": "rgba(249,115,22,0.45)"},
                    ],
                    "threshold": {"line": {"color": "#f1f5f9", "width": 2}, "value": 50},
                },
            )
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(t=40, b=0, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

        if label == 1:
            st.error("**Elevated fatigue** — prioritize sleep and downshift intensity today.")
        else:
            st.success("**Lower fatigue signal** — patterns look closer to recovery for this cohort.")

with tab_why:
    st.markdown("#### Summary")
    st.markdown(st.session_state.get("last_summary", "Click **Update prediction** on the first tab."))
    st.markdown("#### What shaped this result?")
    for r in st.session_state.get("last_reasons", []):
        reason_card(r.icon, r.title, r.detail, r.tone)

    st.markdown("#### Your values vs cohort median")
    compare = pd.DataFrame(
        {
            "You": [st.session_state.row[c] for c in FEATURE_COLUMNS],
            "Cohort median": [defaults[c] for c in FEATURE_COLUMNS],
        },
        index=[c.replace("_", " ").title() for c in FEATURE_COLUMNS],
    )
    st.bar_chart(compare, color=["#a855f7", "#64748b"], stack=False)

with tab_data:
    st.dataframe(df[FEATURE_COLUMNS + ["fatigue_high"]].head(25), use_container_width=True, height=400)
