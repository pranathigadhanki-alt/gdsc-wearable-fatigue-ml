"""What-if scenarios for the demo UI."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.pipeline import Pipeline

from solutions.baselines import watch_row_with_deltas
from solutions.models import FEATURE_COLUMNS, predict_strain


@dataclass
class WhatIf:
    title: str
    detail: str
    proba: float
    delta_pp: float  # percentage points vs current


def suggest_what_ifs(
    participant_id,
    today: dict,
    baselines,
    pipe: Pipeline,
    current_proba: float,
) -> list[WhatIf]:
    base_row = watch_row_with_deltas(participant_id, today, baselines)
    _, p0 = predict_strain(base_row, pipe)
    scenarios = [
        ("sleep_duration", +1.0, "🌙 Sleep 1 hour longer", "Same day, but you got an extra hour of sleep."),
        ("sleep_duration", +1.5, "🌙 Catch-up sleep night", "A stronger recovery night than today."),
        ("daily_steps", +2000, "🚶 Walk 2,000 more steps", "Light movement often tracks with better recovery signals."),
        ("daily_steps", +4000, "🚶 Active recovery day", "Much more movement than today."),
        ("heart_rate", -5, "❤️ Calmer resting heart rate", "As if your body were 5 bpm more relaxed at rest."),
    ]
    out: list[WhatIf] = []
    for key, change, title, detail in scenarios:
        tweaked = dict(today)
        tweaked[key] = tweaked[key] + change
        if key == "sleep_duration":
            tweaked[key] = min(9.0, max(5.0, tweaked[key]))
        if key == "daily_steps":
            tweaked[key] = min(15000, max(1000, tweaked[key]))
        if key == "heart_rate":
            tweaked[key] = min(95, max(55, tweaked[key]))
        row = watch_row_with_deltas(participant_id, tweaked, baselines)
        _, proba = predict_strain(row, pipe)
        out.append(
            WhatIf(
                title=title,
                detail=detail,
                proba=proba,
                delta_pp=(proba - p0) * 100,
            )
        )
    out.sort(key=lambda x: x.delta_pp)
    return out[:4]
