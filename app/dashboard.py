"""Shared Streamlit UI — mentees use via `streamlit_app.py`, mentors via `mentor_preview.py`."""

from __future__ import annotations

from typing import Callable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.input_helpers import (
    COMPARE_LABELS,
    UI_DEFAULT_KEYS,
    ui_to_explain_row,
    ui_to_model_row,
)
from app.ui_theme import hero, inject_theme, reason_card

PRESETS = {
    "Custom (sliders)": None,
    "📚 Crunch week": {
        "sleep_duration": 5.8,
        "quality_of_sleep": 4,
        "stress_level": 8,
        "physical_activity_level": 25,
        "heart_rate": 82,
        "daily_steps": 3500,
        "age": 22,
    },
    "😴 Recovery day": {
        "sleep_duration": 8.0,
        "quality_of_sleep": 9,
        "stress_level": 3,
        "physical_activity_level": 55,
        "heart_rate": 64,
        "daily_steps": 9000,
        "age": 22,
    },
    "🏃 Active, short sleep": {
        "sleep_duration": 6.0,
        "quality_of_sleep": 6,
        "stress_level": 7,
        "physical_activity_level": 85,
        "heart_rate": 78,
        "daily_steps": 12000,
        "age": 28,
    },
}


def _default_ui(df: pd.DataFrame, feature_columns: list[str]) -> dict:
    med = df[feature_columns].median()
    ui = {
        "sleep_duration": float(med["sleep_duration"]),
        "quality_of_sleep": int(med["quality_of_sleep"]),
        "heart_rate": int(med["heart_rate"]),
        "physical_activity_level": int(med["physical_activity_level"]),
        "daily_steps": int(med["daily_steps"]),
        "age": int(med["age"]),
    }
    if "stress_level" in df.columns:
        ui["stress_level"] = int(df["stress_level"].median())
    else:
        ui["stress_level"] = 5
    return ui


def run_dashboard(
    *,
    load_feature_table: Callable,
    feature_columns: list[str],
    train_model: Callable,
    save_model: Callable,
    predict_fatigue: Callable,
    explain_prediction: Callable,
    subtitle: str = "See how sleep, stress, and heart rate combine — with a plain-language explanation.",
) -> None:
    st.set_page_config(
        page_title="Fatigue Insight",
        page_icon="💤",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()

    @st.cache_resource
    def get_model_and_data():
        df = load_feature_table(use_demo=True)
        pipe = train_model(use_demo=True)
        save_model(pipe)
        return pipe, df

    pipe, df = get_model_and_data()
    defaults_ui = _default_ui(df, feature_columns)
    medians_ui = dict(defaults_ui)

    with st.sidebar:
        st.markdown("### 🎛️ Quick scenarios")
        preset_name = st.selectbox("Load a profile", list(PRESETS.keys()))
        st.markdown("---")
        st.caption("Educational demo — not medical advice.")
        st.metric("Rows in table", len(df))
        st.metric("High fatigue %", f"{df['fatigue_high'].mean():.0%}")

    hero("Stress & Fatigue Insight", subtitle)

    if "ui" not in st.session_state:
        st.session_state.ui = defaults_ui

    if PRESETS[preset_name] is not None:
        st.session_state.ui = dict(PRESETS[preset_name])
        st.session_state.pop("last_proba", None)

    tab_input, tab_why, tab_data = st.tabs(["✨ Your day", "💬 Why this score?", "📊 Cohort data"])

    with tab_input:
        left, mid, right = st.columns([1.1, 1, 1])
        ui = st.session_state.ui

        with left:
            st.markdown("#### Sleep & stress")
            ui["sleep_duration"] = st.slider(
                "🌙 Sleep last night (hours)",
                5.0,
                9.0,
                float(ui.get("sleep_duration", medians_ui["sleep_duration"])),
                0.1,
                help="How long you slept — from your watch or best guess.",
            )
            ui["quality_of_sleep"] = st.slider(
                "✨ How rested do you feel? (1–10)",
                1,
                10,
                int(ui.get("quality_of_sleep", medians_ui["quality_of_sleep"])),
                help="1 = exhausted, 10 = fully refreshed.",
            )
            ui["stress_level"] = st.slider(
                "⚡ Stress right now (1–10)",
                1,
                10,
                int(ui.get("stress_level", medians_ui["stress_level"])),
                help="1 = calm, 10 = very stressed. No math — we combine this with sleep for the model.",
            )

        with mid:
            st.markdown("#### Body & activity")
            ui["heart_rate"] = st.slider(
                "❤️ Resting heart rate (bpm)",
                55,
                95,
                int(ui.get("heart_rate", medians_ui["heart_rate"])),
            )
            ui["physical_activity_level"] = st.slider(
                "🏃 Active minutes yesterday",
                0,
                100,
                int(ui.get("physical_activity_level", medians_ui["physical_activity_level"])),
            )
            ui["daily_steps"] = st.slider(
                "🚶 Steps yesterday",
                1000,
                15000,
                int(ui.get("daily_steps", medians_ui["daily_steps"])),
                500,
            )
            ui["age"] = st.slider("🎂 Age", 18, 70, int(ui.get("age", medians_ui["age"])))
            st.session_state.ui = ui
            run = st.button("🔮 Update prediction", type="primary", use_container_width=True)

        with right:
            model_row = ui_to_model_row(ui)
            explain_row = ui_to_explain_row(ui, model_row)

            if run or "last_proba" not in st.session_state:
                label, proba = predict_fatigue(model_row, pipe)
                reasons, summary = explain_prediction(explain_row, df, pipe, label, proba)
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
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(t=40, b=0, l=20, r=20),
            )
            st.plotly_chart(fig, use_container_width=True)

            if label == 1:
                st.error("**Elevated fatigue** — prioritize sleep and downshift intensity today.")
            else:
                st.success("**Lower fatigue signal** — patterns look closer to recovery for this cohort.")

    with tab_why:
        st.markdown("#### Summary")
        st.markdown(st.session_state.get("last_summary", "Click **Update prediction** on the first tab."))
        st.markdown("#### Why we think that")
        for r in st.session_state.get("last_reasons", []):
            reason_card(r.icon, r.title, r.detail, r.tone)

        st.markdown("#### You vs typical in our dataset")
        ui = st.session_state.ui
        cohort = medians_ui
        compare = pd.DataFrame(
            {
                "You": [ui[k] for k in COMPARE_LABELS],
                "Typical": [cohort[k] for k in COMPARE_LABELS],
            },
            index=list(COMPARE_LABELS.values()),
        )
        st.bar_chart(compare, color=["#a855f7", "#64748b"], stack=False)

    with tab_data:
        show_cols = feature_columns + ["fatigue_high"]
        if "stress_level" in df.columns:
            show_cols = ["stress_level"] + show_cols
        st.dataframe(df[show_cols].head(25), use_container_width=True, height=400)
