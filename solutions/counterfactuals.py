"""What-if: what increases chance of a better night tomorrow?"""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.pipeline import Pipeline

from solutions.baselines import build_model_row
from solutions.models import predict_recovery


@dataclass
class WhatIf:
    title: str
    detail: str
    proba: float
    delta_pp: float


def suggest_what_ifs(
    participant_id,
    today: dict,
    last_night: dict,
    baselines,
    pipe: Pipeline,
    current_proba: float,
) -> list[WhatIf]:
    base_row = build_model_row(participant_id, today, last_night, baselines)
    _, p0 = predict_recovery(base_row, pipe)

    scenarios = [
        ("sleep_duration", +1.0, "🌙 Go to bed 1 hour earlier", "Give your body more time to recover."),
        ("sleep_duration", +1.5, "🌙 Protect a longer sleep window", "Especially helpful after a short night."),
        ("daily_steps", +2000, "🚶 Add a 20–30 min walk", "Light movement — not exhaustive training."),
        ("daily_steps", +4000, "🚶 Active but gentle day", "More steps than today’s plan."),
        ("heart_rate", -4, "❤️ Calmer evening routine", "As if resting HR settled 4 bpm lower (wind-down, hydration)."),
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
        row = build_model_row(participant_id, tweaked, last_night, baselines)
        _, proba = predict_recovery(row, pipe)
        out.append(WhatIf(title=title, detail=detail, proba=proba, delta_pp=(proba - p0) * 100))
    out.sort(key=lambda x: -x.delta_pp)
    return out[:4]
