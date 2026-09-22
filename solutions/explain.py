"""Plain-language fatigue explanations for the demo UI."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from solutions.models import FEATURE_COLUMNS

# Human labels for UI
FEATURE_LABELS = {
    "sleep_duration": "Sleep duration",
    "quality_of_sleep": "Sleep quality",
    "physical_activity_level": "Daily activity",
    "heart_rate": "Resting heart rate",
    "daily_steps": "Step count",
    "age": "Age",
    "stress_x_poor_sleep": "Stress × poor sleep",
}


@dataclass
class Reason:
    icon: str
    tone: str  # risk | ok | neutral
    title: str
    detail: str


def rule_reasons(row: dict, reference: pd.DataFrame) -> list[Reason]:
    """Rule-based narrative aligned with how we label fatigue in features.py."""
    reasons: list[Reason] = []
    med = reference[FEATURE_COLUMNS].median()

    q = row.get("quality_of_sleep", med["quality_of_sleep"])
    if q <= 5:
        reasons.append(
            Reason(
                "🌙",
                "risk",
                "Sleep quality is low",
                f"Quality score is {q}/10. Poor sleep is one of the strongest fatigue cues in this dataset.",
            )
        )
    elif q >= 8:
        reasons.append(
            Reason(
                "🌙",
                "ok",
                "Sleep quality looks solid",
                f"Quality score is {q}/10, which usually supports recovery.",
            )
        )

    stress_proxy = row.get("stress_x_poor_sleep", 0)
    if stress_proxy >= 35:
        reasons.append(
            Reason(
                "⚡",
                "risk",
                "Stress and sleep are interacting",
                "High stress combined with poor sleep pushes the model toward fatigue.",
            )
        )
    elif stress_proxy <= 15:
        reasons.append(
            Reason(
                "⚡",
                "ok",
                "Stress load looks manageable",
                "Stress × sleep interaction is in a lower range for this cohort.",
            )
        )

    hr = row.get("heart_rate", med["heart_rate"])
    if hr >= med["heart_rate"] + 8:
        reasons.append(
            Reason(
                "❤️",
                "risk",
                "Heart rate is elevated",
                f"{hr:.0f} bpm is above the demo median (~{med['heart_rate']:.0f} bpm), "
                "which can track with stress or under-recovery.",
            )
        )

    sleep_h = row.get("sleep_duration", med["sleep_duration"])
    if sleep_h < 6.2:
        reasons.append(
            Reason(
                "⏰",
                "risk",
                "Short sleep window",
                f"{sleep_h:.1f} hours is below what most rows in the dataset report.",
            )
        )
    elif sleep_h >= 7.5:
        reasons.append(
            Reason(
                "⏰",
                "ok",
                "Adequate time in bed",
                f"{sleep_h:.1f} hours supports recovery for many people in the sample.",
            )
        )

    steps = row.get("daily_steps", med["daily_steps"])
    if steps < 4000:
        reasons.append(
            Reason(
                "🚶",
                "neutral",
                "Low movement day",
                "Fewer steps can mean rest — or reduced energy; context matters.",
            )
        )

    return reasons


def model_reasons(row: dict, pipe: Pipeline) -> list[Reason]:
    """Top feature importances from the trained forest (global + this row direction)."""
    clf = pipe.named_steps.get("clf")
    if clf is None or not hasattr(clf, "feature_importances_"):
        return []

    imps = pd.Series(clf.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
    top = imps.head(3)
    out: list[Reason] = []
    for name, imp in top.items():
        label = FEATURE_LABELS.get(name, name)
        val = row.get(name, 0)
        out.append(
            Reason(
                "🧠",
                "neutral",
                f"Model weighs «{label}»",
                f"Importance {imp:.0%} in the forest. Your value here: {val:.1f}.",
            )
        )
    return out


def build_summary(label: int, proba: float, reasons: list[Reason]) -> str:
    risk = [r for r in reasons if r.tone == "risk"]
    ok = [r for r in reasons if r.tone == "ok"]

    if label == 1:
        lead = (
            f"The model estimates a **{proba:.0%}** chance of **elevated fatigue** "
            "based on sleep, stress, and heart-rate patterns like those in the Kaggle dataset."
        )
    else:
        lead = (
            f"The model estimates a **{proba:.0%}** chance of elevated fatigue — "
            "currently closer to a **typical recovery** profile for this demo cohort."
        )

    if risk:
        because = " Main drivers in your profile: " + "; ".join(r.title.lower() for r in risk[:3]) + "."
    elif ok:
        because = " Supportive signals include: " + "; ".join(r.title.lower() for r in ok[:2]) + "."
    else:
        because = " Inputs are near cohort averages — the score reflects subtle combinations of features."

    return lead + because


def explain_prediction(
    row: dict,
    reference: pd.DataFrame,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list[Reason], str]:
    rules = rule_reasons(row, reference)
    model = model_reasons(row, pipe)
    # De-duplicate by title
    seen = set()
    merged: list[Reason] = []
    for r in rules + model:
        if r.title in seen:
            continue
        seen.add(r.title)
        merged.append(r)
    summary = build_summary(label, proba, merged)
    return merged, summary
