"""Recovery-focused copy — vs your baseline, disorder-aware."""

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
    b = baselines[baselines["participant_id"] == participant_id]
    if b.empty:
        b = baselines.iloc[[0]]
    b = b.iloc[0]
    disorder = str(b.get("sleep_disorder", "Insomnia"))

    reasons.append(
        Reason(
            "🩺",
            "neutral",
            f"Profile: {disorder}",
            "We train on public data from people with **insomnia** or **sleep apnea** — "
            "this is education, not a diagnosis or sleep study.",
        )
    )

    sd = float(model_row.get("sleep_duration_delta", 0))
    if sd <= -0.4:
        reasons.append(
            Reason(
                "🌙",
                "risk",
                "Less sleep than your usual",
                f"Tonight is about **{abs(sd):.1f} h** below *your* normal — recovery nights are harder to stack after short sleep.",
            )
        )
    elif sd >= 0.4:
        reasons.append(
            Reason(
                "🌙",
                "ok",
                "Extra sleep vs your baseline",
                "More time in bed than your typical night — that often helps the **next** night go better.",
            )
        )

    lag_sleep = float(model_row.get("lag1_sleep_duration", 0))
    if lag_sleep < float(b["sleep_duration"]) - 0.5:
        reasons.append(
            Reason(
                "📅",
                "risk",
                "Rough previous night",
                f"Last night’s sleep was short (**{lag_sleep:.1f} h**). The model uses that history — not how you *feel* today.",
            )
        )

    hr_d = float(model_row.get("heart_rate_delta", 0))
    if hr_d >= 6:
        reasons.append(
            Reason(
                "❤️",
                "risk",
                "Resting HR above your norm",
                f"**{hr_d:.0f} bpm** above your baseline — common in apnea/insomnia flares in this dataset.",
            )
        )

    steps_d = float(model_row.get("daily_steps_delta", 0))
    if steps_d >= 1500:
        reasons.append(
            Reason(
                "🚶",
                "ok",
                "More movement than usual",
                "Higher activity vs *your* baseline sometimes aligns with better recovery nights in the data.",
            )
        )

    if proba >= 0.55:
        lead = (
            f"About **{proba:.0%}** chance of a **better night tomorrow** "
            "(more sleep or better-rest feeling in the data) given tonight’s watch-like signals."
        )
    else:
        lead = (
            f"About **{proba:.0%}** chance of a clear recovery night tomorrow — "
            "patterns look tougher from here; small habit shifts may still help (see What-if)."
        )

    risk = [r for r in reasons if r.tone == "risk"]
    if risk:
        tail = " Headwinds: **" + "**, **".join(r.title for r in risk[:2]) + "**."
    else:
        tail = " Signals are relatively aligned with recovery in this profile."

    return reasons, lead + tail
