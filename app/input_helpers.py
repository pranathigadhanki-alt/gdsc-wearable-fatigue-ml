from solutions.baselines import build_model_row
from src.kaggle_schema import WATCH_SIGNALS

COMPARE_LABELS = {
    "sleep_duration": "Tonight sleep (h)",
    "heart_rate": "Resting HR",
    "daily_steps": "Steps today",
    "physical_activity_level": "Active min",
}


def ui_to_model_row(participant_id, today: dict, last_night: dict, baselines) -> dict:
    return build_model_row(participant_id, today, last_night, baselines)
