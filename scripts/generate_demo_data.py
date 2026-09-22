#!/usr/bin/env python3
"""Longitudinal demo data: multiple «nights» per person for real baselines."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solutions.baselines import compute_person_baselines
from solutions.features import build_features_from_kaggle, strain_label

RNG = np.random.default_rng(42)
OUT = ROOT / "data" / "sample_demo.csv"
BASE_OUT = ROOT / "data" / "person_baselines.csv"


def main() -> None:
    rows = []
    for pid in range(1, 41):
        base_sleep = float(RNG.normal(7.2, 0.4))
        base_hr = float(RNG.normal(68, 4))
        base_steps = float(RNG.normal(7500, 1200))
        for _ in range(12):
            sleep = base_sleep + float(RNG.normal(0, 0.6))
            hr = base_hr + float(RNG.normal(0, 4))
            steps = base_steps + float(RNG.normal(0, 1500))
            quality = int(np.clip(RNG.normal(7, 1.5), 3, 10))
            stress = int(np.clip(RNG.normal(5, 2), 2, 10))
            if sleep < 6.0:
                stress = min(10, stress + 2)
                quality = max(3, quality - 2)
            rows.append(
                {
                    "Person ID": pid,
                    "Gender": "Female" if pid % 2 else "Male",
                    "Age": 20 + (pid % 15),
                    "Occupation": "Student",
                    "Sleep Duration": sleep,
                    "Quality of Sleep": quality,
                    "Physical Activity Level": int(np.clip(RNG.normal(45, 15), 10, 90)),
                    "Stress Level": stress,
                    "BMI Category": "Normal",
                    "Blood Pressure": "120/80",
                    "Heart Rate": hr,
                    "Daily Steps": int(np.clip(steps, 1500, 14000)),
                    "Sleep Disorder": "None",
                }
            )

    raw = pd.DataFrame(rows)
    feats = build_features_from_kaggle(raw)
    feats["strain_high"] = strain_label(feats)
    baselines = compute_person_baselines(feats)

    keep = [
        "participant_id",
        "sleep_duration",
        "heart_rate",
        "daily_steps",
        "physical_activity_level",
        "sleep_duration_delta",
        "heart_rate_delta",
        "daily_steps_delta",
        "physical_activity_level_delta",
        "strain_high",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    feats[keep].to_csv(OUT, index=False)
    baselines.to_csv(BASE_OUT, index=False)
    print(f"Wrote {len(feats)} rows, {len(baselines)} people → {OUT}")


if __name__ == "__main__":
    main()
