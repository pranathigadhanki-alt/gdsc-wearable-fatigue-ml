"""Plain language: today vs *your* baseline — no survey questions, no ML jargon."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from src.kaggle_schema import WATCH_SIGNALS


@dataclass
class Reason:
    icon: str
    tone: str
    title: str
    detail: str


def _fmt_delta(name: str, delta: float, unit: str) -> Reason | None:
    labels = {
        "sleep_duration": ("Sleep duration", "hours"),
        "heart_rate": ("Resting heart rate", "bpm"),
        "daily_steps": ("Steps", ""),
        "physical_activity_level": ("Active minutes", "min"),
    }
    title, u = labels.get(name, (name, unit))
    if abs(delta) < 0.05 if name == "sleep_duration" else abs(delta) < 30:
        return None
    if delta < 0 and name == "sleep_duration":
        return Reason(
            "🌙",
            "risk",
            "Less sleep than your normal",
            f"About **{abs(delta):.1f} {u}** below *your* usual — the model treats that like higher next-day strain.",
        )
    if delta > 0 and name == "sleep_duration":
        return Reason(
            "🌙",
            "ok",
            "More sleep than your normal",
            f"**{delta:.1f} {u}** above *your* baseline — a recovery-friendly signal.",
        )
    if delta > 5 and name == "heart_rate":
        return Reason(
            "❤️",
            "risk",
            "Heart rate above your baseline",
            f"**{delta:.0f} bpm** higher than your typical resting rate — often shows up before people feel «off».",
        )
    if delta < -3 and name == "heart_rate":
        return Reason(
            "❤️",
            "ok",
            "Calmer than your usual",
            f"**{abs(delta):.0f} bpm** below your normal resting heart rate.",
        )
    if delta < -800 and name == "daily_steps":
        return Reason(
            "🚶",
            "neutral",
            "Much quieter than your norm",
            f"**{abs(delta):,.0f} steps** below your typical day — rest or low energy; context matters.",
        )
    if delta > 1000 and name == "daily_steps":
        return Reason(
            "🚶",
            "ok",
            "More movement than your norm",
            f"**{delta:,.0f} extra steps** vs your baseline.",
        )
    return None


def explain_prediction(
    model_row: dict,
    baselines: pd.DataFrame,
    participant_id,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list[Reason], str]:
    del pipe, label
    reasons: list[Reason] = []
    for col in WATCH_SIGNALS:
        d = model_row.get(f"{col}_delta", 0)
        r = _fmt_delta(col, float(d), "")
        if r:
            reasons.append(r)

    b = baselines[baselines["participant_id"] == participant_id]
    if b.empty:
        b = baselines.iloc[[0]]
    b = b.iloc[0]

    reasons.insert(
        0,
        Reason(
            "👤",
            "neutral",
            "Compared to you — not everyone else",
            f"Your normal: **{b['sleep_duration']:.1f}h sleep**, **{b['heart_rate']:.0f} bpm**, "
            f"**{b['daily_steps']:,.0f} steps**. Today’s score is about deviation from *that*.",
        ),
    )

    if proba >= 0.55:
        lead = (
            f"**{proba:.0%}** estimated chance of **elevated next-day strain** from watch-like signals "
            "— **without** asking how stressed or rested you feel."
        )
    else:
        lead = (
            f"**{proba:.0%}** strain risk — today looks **closer to your own normal** in the data we learned from."
        )

    risk = [r for r in reasons if r.tone == "risk"]
    if risk:
        tail = " Main flags: **" + "**, **".join(r.title for r in risk[:2]) + "**."
    else:
        tail = " No big departures from your baseline — that keeps strain risk lower."

    return reasons, lead + tail
