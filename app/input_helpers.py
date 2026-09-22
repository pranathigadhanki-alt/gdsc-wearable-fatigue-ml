"""Watch-only UI → model row with personal baseline deltas."""

from __future__ import annotations

from solutions.baselines import watch_row_with_deltas
from src.kaggle_schema import WATCH_SIGNALS

COMPARE_LABELS = {
    "sleep_duration": "Sleep (hours)",
    "heart_rate": "Heart rate",
    "daily_steps": "Steps",
    "physical_activity_level": "Active min",
}


def ui_to_model_row(participant_id, today: dict, baselines) -> dict:
    return watch_row_with_deltas(participant_id, today, baselines)
