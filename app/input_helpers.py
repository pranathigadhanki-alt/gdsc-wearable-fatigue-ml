"""Map friendly UI inputs → model feature row (students keep stress_x_poor_sleep in src/features.py only)."""

from __future__ import annotations


def stress_x_poor_sleep(stress_level: float, quality_of_sleep: float) -> float:
    """Same formula as Session 3 feature engineering — computed in the app, not by the user."""
    return float(stress_level) * (10.0 - float(quality_of_sleep))


def ui_to_model_row(ui: dict) -> dict:
    """Build the dict passed to predict_fatigue / the model."""
    q = float(ui["quality_of_sleep"])
    stress = float(ui["stress_level"])
    return {
        "sleep_duration": float(ui["sleep_duration"]),
        "quality_of_sleep": q,
        "physical_activity_level": float(ui["physical_activity_level"]),
        "heart_rate": float(ui["heart_rate"]),
        "daily_steps": float(ui["daily_steps"]),
        "age": float(ui["age"]),
        "stress_x_poor_sleep": stress_x_poor_sleep(stress, q),
    }


def ui_to_explain_row(ui: dict, model_row: dict) -> dict:
    """Explanation rules use readable stress_level + model features."""
    return {**model_row, "stress_level": float(ui["stress_level"])}


# Sliders the user sees (no derived math)
UI_DEFAULT_KEYS = (
    "sleep_duration",
    "quality_of_sleep",
    "stress_level",
    "heart_rate",
    "physical_activity_level",
    "daily_steps",
    "age",
)

# Bar chart on «Why» tab — human-readable only
COMPARE_LABELS = {
    "sleep_duration": "Sleep (hours)",
    "quality_of_sleep": "Sleep quality",
    "stress_level": "Stress level",
    "heart_rate": "Heart rate",
    "daily_steps": "Daily steps",
    "age": "Age",
    "physical_activity_level": "Activity (min)",
}
