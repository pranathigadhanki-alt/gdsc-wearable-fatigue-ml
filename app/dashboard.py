"""StrainScope dashboard — watch signals, personal baseline, what-if."""

from __future__ import annotations

from typing import Callable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.input_helpers import COMPARE_LABELS, ui_to_model_row
from app.ui_theme import baseline_pills, hero, inject_theme, reason_card
from src.kaggle_schema import WATCH_SIGNALS

PRESETS = {
    "Typical day (your baseline)": "baseline",
    "🔥 Short sleep + high HR": "bad",
    "💚 Recovery day": "good",
}


def run_dashboard(
    *,
    load_feature_table: Callable,
    load_person_baselines: Callable,
    feature_columns: list[str],
    train_model: Callable,
    save_model: Callable,
    predict_strain: Callable,
    explain_prediction: Callable,
    suggest_what_ifs: Callable,
    subtitle: str,
) -> None:
    st.set_page_config(page_title="StrainScope", page_icon="⌚", layout="wide", initial_sidebar_state="expanded")
    inject_theme()

    @st.cache_resource
    def get_assets():
        df = load_feature_table(use_demo=True)
        baselines = load_person_baselines(use_demo=True)
        pipe = train_model(use_demo=True)
        save_model(pipe)
        return df, baselines, pipe

    df, baselines, pipe = get_assets()
    people = baselines["participant_id"].tolist()

    with st.sidebar:
        st.markdown("### ⌚ Choose a profile")
        pid = st.selectbox("Person (for *your* baseline)", people, format_func=lambda x: f"Person {x}")
        preset = st.selectbox("Quick today scenario", list(PRESETS.keys()))
        st.markdown("---")
        st.caption("We never ask «how stressed are you?» — only watch-like signals.")
        st.metric("Training nights", len(df))
        st.metric("High strain nights", f"{df['strain_high'].mean():.0%}")

    b = baselines[baselines["participant_id"] == pid].iloc[0]

    hero(
        "StrainScope",
        subtitle,
    )

    if "today" not in st.session_state:
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}
        st.session_state.pid = pid

    if st.session_state.pid != pid:
        st.session_state.pid = pid
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}

    if PRESETS[preset] == "baseline":
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}
    elif PRESETS[preset] == "bad":
        st.session_state.today = {
            "sleep_duration": max(5.0, float(b["sleep_duration"]) - 1.5),
            "heart_rate": min(95, float(b["heart_rate"]) + 12),
            "daily_steps": max(1500, float(b["daily_steps"]) - 3500),
            "physical_activity_level": max(10, float(b["physical_activity_level"]) - 20),
        }
    elif PRESETS[preset] == "good":
        st.session_state.today = {
            "sleep_duration": min(9.0, float(b["sleep_duration"]) + 1.2),
            "heart_rate": max(55, float(b["heart_rate"]) - 8),
            "daily_steps": min(14000, float(b["daily_steps"]) + 2500),
            "physical_activity_level": min(90, float(b["physical_activity_level"]) + 15),
        }

    tab_today, tab_why, tab_whatif, tab_data = st.tabs(
        ["📡 Today’s signals", "💬 Why?", "✨ What moves the needle?", "📊 Data"]
    )

    today = st.session_state.today

    with tab_today:
        st.markdown("#### Your normal (baseline)")
        baseline_pills(float(b["sleep_duration"]), float(b["heart_rate"]), float(b["daily_steps"]))

        c1, c2, c3 = st.columns([1, 1, 1.1])
        with c1:
            today["sleep_duration"] = st.slider(
                "🌙 Sleep (hours)", 5.0, 9.0, float(today["sleep_duration"]), 0.1
            )
            today["heart_rate"] = st.slider(
                "❤️ Resting HR (bpm)", 55, 95, int(today["heart_rate"])
            )
        with c2:
            today["daily_steps"] = st.slider(
                "🚶 Steps", 1000, 15000, int(today["daily_steps"]), 500
            )
            today["physical_activity_level"] = st.slider(
                "🏃 Active minutes", 10, 90, int(today["physical_activity_level"])
            )
        st.session_state.today = today

        model_row = ui_to_model_row(pid, today, baselines)
        run = st.button("🔮 Estimate next-day strain", type="primary", use_container_width=True)

        with c3:
            if run or "proba" not in st.session_state:
                label, proba = predict_strain(model_row, pipe)
                reasons, summary = explain_prediction(
                    model_row, baselines, pid, pipe, label, proba
                )
                whatifs = suggest_what_ifs(pid, today, baselines, pipe, proba)
                st.session_state.update(proba=proba, label=label, summary=summary, reasons=reasons, whatifs=whatifs)

            proba = st.session_state.get("proba", 0.0)
            label = st.session_state.get("label", 0)

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=proba * 100,
                    number={"suffix": "%", "font": {"size": 44, "color": "#f8fafc"}},
                    title={"text": "Next-day strain", "font": {"color": "#e2e8f0", "size": 16}},
                    delta={"reference": 50, "suffix": "%"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#c084fc" if label else "#2dd4bf"},
                        "steps": [
                            {"range": [0, 35], "color": "rgba(45,212,191,0.4)"},
                            {"range": [35, 65], "color": "rgba(250,204,21,0.35)"},
                            {"range": [65, 100], "color": "rgba(251,146,60,0.5)"},
                        ],
                    },
                )
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=280,
                margin=dict(t=50, b=10, l=25, r=25),
            )
            st.plotly_chart(fig, use_container_width=True)
            if label:
                st.error("Patterns look like a **higher-strain** day for this person.")
            else:
                st.success("Closer to **their** normal — lower predicted strain.")

    with tab_why:
        st.markdown(st.session_state.get("summary", "Run estimate on the first tab."))
        for r in st.session_state.get("reasons", []):
            reason_card(r.icon, r.title, r.detail, r.tone)

        st.markdown("#### Today vs your baseline")
        comp = pd.DataFrame(
            {
                "Today": [today[k] for k in WATCH_SIGNALS],
                "Your baseline": [float(b[k]) for k in WATCH_SIGNALS],
            },
            index=[COMPARE_LABELS[k] for k in WATCH_SIGNALS],
        )
        st.bar_chart(comp, color=["#a78bfa", "#64748b"], stack=False)

    with tab_whatif:
        st.markdown(
            "Small changes in **sleep**, **steps**, or **heart rate** — "
            "we re-run the same model and show how strain risk shifts."
        )
        for w in st.session_state.get("whatifs", []):
            sign = "↓" if w.delta_pp < 0 else "↑"
            st.markdown(
                f'<div class="whatif"><strong>{w.title}</strong> — {w.detail}<br>'
                f'Strain risk: <strong>{w.proba:.0%}</strong> '
                f'<span style="color:{"#4ade80" if w.delta_pp < 0 else "#fb923c"};">'
                f'({sign} {abs(w.delta_pp):.0f} pp vs today)</span></div>',
                unsafe_allow_html=True,
            )

    with tab_data:
        st.dataframe(df.head(30), use_container_width=True, height=420)
