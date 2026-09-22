#!/usr/bin/env python3
"""Disorder cohort + longitudinal nights + recovery label."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solutions.baselines import compute_person_baselines
from solutions.features import build_features_from_kaggle, prepare_training_frame

RNG = np.random.default_rng(42)
OUT = ROOT / "data" / "sample_demo.csv"
BASE_OUT = ROOT / "data" / "person_baselines.csv"


def main() -> None:
    rows = []
    for pid in range(1, 41):
        disorder = "Insomnia" if pid <= 20 else "Sleep Apnea"
        base_sleep = 6.2 if disorder == "Insomnia" else 6.6
        base_sleep += float(RNG.normal(0, 0.3))
        base_hr = 70 if disorder == "Sleep Apnea" else 66
        base_hr += float(RNG.normal(0, 3))
        base_steps = float(RNG.normal(6500, 1000))

        prev_sleep, prev_hr, prev_steps, prev_act = base_sleep, base_hr, base_steps, 45.0
        for night in range(14):
            sleep = float(np.clip(prev_sleep + RNG.normal(0, 0.5), 5.0, 9.0))
            hr = float(np.clip(prev_hr + RNG.normal(0, 3), 58, 92))
            steps = int(np.clip(prev_steps + RNG.normal(0, 1200), 1500, 13000))
            act = int(np.clip(40 + RNG.normal(0, 12), 10, 90))
            quality = int(np.clip(5 + (sleep - 6) * 1.2 + RNG.normal(0, 1), 3, 10))
            if disorder == "Sleep Apnea" and sleep < 6.5:
                hr += 4
                quality = max(3, quality - 1)

            rows.append(
                {
                    "Person ID": pid,
                    "Gender": "Female" if pid % 2 else "Male",
                    "Age": 22 + (pid % 20),
                    "Occupation": "Student",
                    "Sleep Duration": sleep,
                    "Quality of Sleep": quality,
                    "Physical Activity Level": act,
                    "Stress Level": int(np.clip(8 - quality // 2 + RNG.integers(0, 3), 2, 10)),
                    "BMI Category": "Overweight" if disorder == "Sleep Apnea" else "Normal",
                    "Blood Pressure": "130/85" if disorder == "Sleep Apnea" else "120/80",
                    "Heart Rate": hr,
                    "Daily Steps": steps,
                    "Sleep Disorder": disorder,
                }
            )
            prev_sleep, prev_hr, prev_steps, prev_act = sleep, hr, steps, act

    raw = pd.DataFrame(rows)
    feats = build_features_from_kaggle(raw)
    train = prepare_training_frame(feats)
    baselines = compute_person_baselines(feats)

    keep = [
        "participant_id",
        "sleep_disorder",
        "disorder_insomnia",
        "disorder_apnea",
        "sleep_duration",
        "heart_rate",
        "daily_steps",
        "physical_activity_level",
        "sleep_duration_delta",
        "heart_rate_delta",
        "daily_steps_delta",
        "physical_activity_level_delta",
        "lag1_sleep_duration",
        "lag1_heart_rate",
        "lag1_daily_steps",
        "lag1_physical_activity_level",
        "better_night_tomorrow",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    train[keep].to_csv(OUT, index=False)
    baselines.to_csv(BASE_OUT, index=False)
    print(f"Wrote {len(train)} training rows ({train['sleep_disorder'].value_counts().to_dict()})")


if __name__ == "__main__":
    main()
