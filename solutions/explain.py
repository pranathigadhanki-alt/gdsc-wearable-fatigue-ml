"""Plain-language fatigue explanations for the demo UI — no ML jargon."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from solutions.models import FEATURE_COLUMNS


@dataclass
class Reason:
    icon: str
    tone: str  # risk | ok | neutral
    title: str
    detail: str


def rule_reasons(row: dict, reference: pd.DataFrame) -> list[Reason]:
    """Everyday reasons a day might feel fine or draining."""
    reasons: list[Reason] = []
    med = reference[FEATURE_COLUMNS].median()

    q = float(row.get("quality_of_sleep", med["quality_of_sleep"]))
    if q <= 5:
        reasons.append(
            Reason(
                "🌙",
                "risk",
                "You didn’t feel well rested",
                f"You rated how rested you feel at **{q:.0f}/10**. Under **6** often shows up on high-fatigue days in our sample.",
            )
        )
    elif q >= 8:
        reasons.append(
            Reason(
                "🌙",
                "ok",
                "Sleep felt restorative",
                f"**{q:.0f}/10** on «how rested you feel» is a strong recovery signal.",
            )
        )

    stress = float(row.get("stress_level", 5))
    if stress >= 7:
        reasons.append(
            Reason(
                "⚡",
                "risk",
                "Stress is running high",
                f"**{stress:.0f}/10** stress is in the range where people often feel worn down the next day.",
            )
        )
    elif stress <= 4:
        reasons.append(
            Reason(
                "⚡",
                "ok",
                "Stress is relatively low",
                f"At **{stress:.0f}/10**, stress isn’t a big drag on your score right now.",
            )
        )

    if stress >= 6 and q <= 5:
        reasons.append(
            Reason(
                "🔗",
                "risk",
                "Stressful day on top of poor sleep",
                "When stress is up **and** sleep felt poor, fatigue tends to spike — that’s the main pattern we teach in this project.",
            )
        )

    hr = float(row.get("heart_rate", med["heart_rate"]))
    hr_med = float(med["heart_rate"])
    if hr >= hr_med + 8:
        reasons.append(
            Reason(
                "❤️",
                "risk",
                "Resting heart rate is up",
                f"**{hr:.0f} bpm** is higher than a typical **{hr_med:.0f} bpm** in our data — sometimes linked to stress or not fully recovering.",
            )
        )
    elif hr <= hr_med - 5:
        reasons.append(
            Reason(
                "❤️",
                "ok",
                "Heart rate looks calm",
                f"**{hr:.0f} bpm** is on the lower side compared with the sample average.",
            )
        )

    sleep_h = float(row.get("sleep_duration", med["sleep_duration"]))
    if sleep_h < 6.2:
        reasons.append(
            Reason(
                "⏰",
                "risk",
                "Not much sleep time",
                f"About **{sleep_h:.1f} hours** is short compared with people who report lower fatigue here.",
            )
        )
    elif sleep_h >= 7.5:
        reasons.append(
            Reason(
                "⏰",
                "ok",
                "Solid hours of sleep",
                f"**{sleep_h:.1f} hours** gives your body time to recover.",
            )
        )

    steps = float(row.get("daily_steps", med["daily_steps"]))
    steps_med = float(med["daily_steps"])
    if steps < 4000:
        reasons.append(
            Reason(
                "🚶",
                "neutral",
                "Quiet day for movement",
                f"**{steps:,.0f} steps** is below a typical **{steps_med:,.0f}** — could be rest, or low energy; only you know which.",
            )
        )
    elif steps >= steps_med * 1.2:
        reasons.append(
            Reason(
                "🚶",
                "ok",
                "You were fairly active",
                f"**{steps:,.0f} steps** is above average in our sample.",
            )
        )

    activity = float(row.get("physical_activity_level", med["physical_activity_level"]))
    act_med = float(med["physical_activity_level"])
    if activity < act_med * 0.7:
        reasons.append(
            Reason(
                "🏃",
                "neutral",
                "Less active minutes than usual",
                f"**{activity:.0f} min** of activity is lower than a typical **{act_med:.0f} min** in the dataset.",
            )
        )

    return reasons


def build_summary(label: int, proba: float, reasons: list[Reason]) -> str:
    risk = [r for r in reasons if r.tone == "risk"]
    ok = [r for r in reasons if r.tone == "ok"]

    if label == 1:
        lead = (
            f"We’re reading about **{proba:.0%}** likelihood of **elevated fatigue** "
            "from how your sleep, stress, and body signals look together."
        )
    else:
        lead = (
            f"About **{proba:.0%}** likelihood of elevated fatigue — "
            "your inputs look **closer to a recovery day** for this demo group."
        )

    if risk:
        because = " Biggest factors: **" + "**, **".join(r.title for r in risk[:3]) + "**."
    elif ok:
        because = " What’s helping: **" + "**, **".join(r.title for r in ok[:2]) + "**."
    else:
        because = " Nothing stands out as extreme — your score is driven by small combinations of sleep and stress."

    return lead + because


def explain_prediction(
    row: dict,
    reference: pd.DataFrame,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list[Reason], str]:
    del pipe  # explanations are human-first; model score already reflects patterns
    reasons = rule_reasons(row, reference)
    summary = build_summary(label, proba, reasons)
    return reasons, summary
