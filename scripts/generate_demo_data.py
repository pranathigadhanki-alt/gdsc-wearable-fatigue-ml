#!/usr/bin/env python3
"""Create sample_demo.csv (Kaggle-like schema) for Sessions 1–2 before download."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solutions.features import build_features_from_kaggle, fatigue_label

RNG = np.random.default_rng(42)
OUT = ROOT / "data" / "sample_demo.csv"


def main() -> None:
    n = 200
    raw = pd.DataFrame(
        {
            "Person ID": range(1, n + 1),
            "Gender": RNG.choice(["Male", "Female"], n),
            "Age": RNG.integers(22, 60, n),
            "Occupation": "Student",
            "Sleep Duration": RNG.normal(7.0, 1.0, n).clip(5, 9),
            "Quality of Sleep": RNG.integers(4, 10, n),
            "Physical Activity Level": RNG.integers(20, 90, n),
            "Stress Level": RNG.integers(3, 10, n),
            "BMI Category": "Normal",
            "Blood Pressure": "120/80",
            "Heart Rate": RNG.integers(60, 90, n),
            "Daily Steps": RNG.integers(3000, 12000, n),
            "Sleep Disorder": "None",
        }
    )
    feats = build_features_from_kaggle(raw)
    feats["fatigue_high"] = fatigue_label(feats)
    cols = [
        "participant_id",
        "sleep_duration",
        "quality_of_sleep",
        "physical_activity_level",
        "stress_level",
        "heart_rate",
        "daily_steps",
        "age",
        "gender_male",
        "stress_x_poor_sleep",
        "fatigue_high",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    feats[cols].to_csv(OUT, index=False)
    print(f"Wrote {len(feats)} rows to {OUT}")


if __name__ == "__main__":
    main()
