"""RecoveryScope — disorder cohort, lags, better night tomorrow."""

from __future__ import annotations

from typing import Callable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.input_helpers import COMPARE_LABELS, ui_to_model_row
from app.ui_theme import baseline_pills, hero, inject_theme, reason_card
from src.kaggle_schema import WATCH_SIGNALS

PRESETS = {
    "Typical night": "baseline",
    "😵 Rough night (short sleep)": "bad",
    "💚 Recovery plan night": "good",
}


def run_dashboard(
    *,
    load_feature_table: Callable,
    load_person_baselines: Callable,
    feature_columns: list[str],
    train_model: Callable,
    save_model: Callable,
    predict_recovery: Callable,
    explain_prediction: Callable,
    suggest_what_ifs: Callable,
    subtitle: str,
) -> None:
    st.set_page_config(page_title="RecoveryScope", page_icon="🌙", layout="wide", initial_sidebar_state="expanded")
    inject_theme()

    @st.cache_resource
    def get_assets():
        df = load_feature_table(use_demo=True)
        baselines = load_person_baselines(use_demo=True)
        pipe = train_model(use_demo=True)
        save_model(pipe)
        return df, baselines, pipe

    df, baselines, pipe = get_assets()
    baselines = baselines[baselines["sleep_disorder"].isin(["Insomnia", "Sleep Apnea"])]
    people = baselines["participant_id"].tolist()

    with st.sidebar:
        st.markdown("### 🩺 Insomnia & sleep apnea profiles")
        pid = st.selectbox(
            "Person",
            people,
            format_func=lambda x: f"Person {x} ({baselines.loc[baselines.participant_id==x,'sleep_disorder'].iloc[0]})",
        )
        preset = st.selectbox("Tonight scenario", list(PRESETS.keys()))
        st.markdown("---")
        st.caption("Not a sleep study or diagnosis — educational ML on public data.")
        st.metric("Training nights", len(df))
        st.metric("Better-tomorrow rate", f"{df['better_night_tomorrow'].mean():.0%}")

    b = baselines[baselines["participant_id"] == pid].iloc[0]
    disorder = str(b["sleep_disorder"])

    hero("RecoveryScope", subtitle)

    if "today" not in st.session_state:
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}
        st.session_state.last_night = {k: float(b[k]) for k in WATCH_SIGNALS}
        st.session_state.pid = pid

    if st.session_state.pid != pid:
        st.session_state.pid = pid
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}
        st.session_state.last_night = {k: float(b[k]) for k in WATCH_SIGNALS}

    if PRESETS[preset] == "baseline":
        st.session_state.today = {k: float(b[k]) for k in WATCH_SIGNALS}
        st.session_state.last_night = {k: float(b[k]) for k in WATCH_SIGNALS}
    elif PRESETS[preset] == "bad":
        st.session_state.last_night = {
            "sleep_duration": max(5.0, float(b["sleep_duration"]) - 1.8),
            "heart_rate": min(95, float(b["heart_rate"]) + 10),
            "daily_steps": max(1500, float(b["daily_steps"]) - 3000),
            "physical_activity_level": max(10, float(b["physical_activity_level"]) - 15),
        }
        st.session_state.today = {
            "sleep_duration": max(5.0, float(b["sleep_duration"]) - 1.2),
            "heart_rate": min(95, float(b["heart_rate"]) + 8),
            "daily_steps": max(1500, float(b["daily_steps"]) - 2000),
            "physical_activity_level": max(10, float(b["physical_activity_level"]) - 10),
        }
    elif PRESETS[preset] == "good":
        st.session_state.today = {
            "sleep_duration": min(9.0, float(b["sleep_duration"]) + 1.0),
            "heart_rate": max(55, float(b["heart_rate"]) - 6),
            "daily_steps": min(14000, float(b["daily_steps"]) + 2000),
            "physical_activity_level": min(90, float(b["physical_activity_level"]) + 12),
        }
        st.session_state.last_night = {k: float(b[k]) for k in WATCH_SIGNALS}

    tab_today, tab_why, tab_whatif, tab_data = st.tabs(
        ["📡 Tonight", "💬 Why?", "✨ Get better tomorrow", "📊 Data"]
    )

    today = st.session_state.today
    last_night = st.session_state.last_night

    with tab_today:
        st.markdown(f"**Disorder context:** {disorder} · compared to *your* baseline")
        baseline_pills(float(b["sleep_duration"]), float(b["heart_rate"]), float(b["daily_steps"]))

        c1, c2, c3 = st.columns([1, 1, 1.05])
        with c1:
            st.markdown("##### Last night (history)")
            last_night["sleep_duration"] = st.slider(
                "🌙 Last night sleep (h)", 5.0, 9.0, float(last_night["sleep_duration"]), 0.1
            )
            last_night["heart_rate"] = st.slider(
                "❤️ Last night HR", 55, 95, int(last_night["heart_rate"])
            )
        with c2:
            st.markdown("##### Tonight / today")
            today["sleep_duration"] = st.slider(
                "🌙 Tonight sleep plan (h)", 5.0, 9.0, float(today["sleep_duration"]), 0.1
            )
            today["heart_rate"] = st.slider("❤️ Resting HR now", 55, 95, int(today["heart_rate"]))
            today["daily_steps"] = st.slider("🚶 Steps today", 1000, 15000, int(today["daily_steps"]), 500)
            today["physical_activity_level"] = st.slider(
                "🏃 Active min", 10, 90, int(today["physical_activity_level"])
            )
            last_night["daily_steps"] = st.slider(
                "🚶 Last night steps", 1000, 15000, int(last_night["daily_steps"]), 500, key="lag_steps"
            )
            last_night["physical_activity_level"] = st.slider(
                "🏃 Last night active min", 10, 90, int(last_night["physical_activity_level"]), key="lag_act"
            )
        st.session_state.today = today
        st.session_state.last_night = last_night

        model_row = ui_to_model_row(pid, today, last_night, baselines)
        run = st.button("🔮 Chance of better night tomorrow", type="primary", use_container_width=True)

        with c3:
            if run or "proba" not in st.session_state:
                label, proba = predict_recovery(model_row, pipe)
                reasons, summary = explain_prediction(model_row, baselines, pid, pipe, label, proba)
                whatifs = suggest_what_ifs(pid, today, last_night, baselines, pipe, proba)
                st.session_state.update(
                    proba=proba, label=label, summary=summary, reasons=reasons, whatifs=whatifs
                )

            proba = st.session_state.get("proba", 0.0)
            label = st.session_state.get("label", 0)

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=proba * 100,
                    number={"suffix": "%", "font": {"size": 44, "color": "#f8fafc"}},
                    title={"text": "Better night tomorrow", "font": {"color": "#e2e8f0", "size": 16}},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#2dd4bf" if label else "#c084fc"},
                        "steps": [
                            {"range": [0, 40], "color": "rgba(251,146,60,0.45)"},
                            {"range": [40, 65], "color": "rgba(250,204,21,0.35)"},
                            {"range": [65, 100], "color": "rgba(45,212,191,0.45)"},
                        ],
                    },
                )
            )
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(t=50, b=10, l=25, r=25))
            st.plotly_chart(fig, use_container_width=True)
            if label:
                st.success("Tomorrow looks **recovery-likely** from these signals.")
            else:
                st.warning("Recovery tomorrow looks **uncertain** — try What-if levers.")

    with tab_why:
        st.markdown(st.session_state.get("summary", "Run the estimate on the Tonight tab."))
        for r in st.session_state.get("reasons", []):
            reason_card(r.icon, r.title, r.detail, r.tone)
        comp = pd.DataFrame(
            {"Tonight": [today[k] for k in WATCH_SIGNALS], "Your baseline": [float(b[k]) for k in WATCH_SIGNALS]},
            index=[COMPARE_LABELS[k] for k in WATCH_SIGNALS],
        )
        st.bar_chart(comp, color=["#a78bfa", "#64748b"], stack=False)

    with tab_whatif:
        st.markdown("Which **small changes tonight** increase the chance of a **better night tomorrow**?")
        for w in st.session_state.get("whatifs", []):
            st.markdown(
                f'<div class="whatif"><strong>{w.title}</strong> — {w.detail}<br>'
                f'Better-tomorrow chance: <strong>{w.proba:.0%}</strong> '
                f'<span style="color:#4ade80;">(+{w.delta_pp:.0f} pp vs now)</span></div>',
                unsafe_allow_html=True,
            )

    with tab_data:
        st.dataframe(df.head(40), use_container_width=True, height=420)
