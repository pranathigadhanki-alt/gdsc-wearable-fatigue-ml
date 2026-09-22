#!/usr/bin/env python3
"""Generate synthetic nightly data for teaching when PMData is not available."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import nightly_sleep_features, rule_based_fatigue_label

RNG = np.random.default_rng(42)
OUT = Path(__file__).resolve().parents[1] / "data" / "sample_demo.csv"


def main() -> None:
    rows = []
    for pid in range(1, 11):
        for day in range(1, 31):
            sleep_min = float(RNG.normal(420, 60))
            time_in_bed = sleep_min + float(RNG.normal(45, 15))
            rows.append(
                {
                    "participant_id": f"P{pid:02d}",
                    "date": f"2024-01-{day:02d}",
                    "time_in_bed_min": max(time_in_bed, 300),
                    "sleep_min": max(sleep_min, 240),
                    "rem_min": max(RNG.normal(90, 20), 30),
                    "deep_min": max(RNG.normal(80, 25), 20),
                    "awake_min": max(RNG.normal(30, 10), 5),
                    "resting_hr": float(RNG.normal(62 + pid * 0.3, 5)),
                    "steps": int(max(RNG.normal(8000, 2000), 500)),
                }
            )

    raw = pd.DataFrame(rows)
    feats = nightly_sleep_features(raw)
    feats["fatigue_high"] = rule_based_fatigue_label(feats)
    keep = [
        "participant_id",
        "date",
        "sleep_efficiency",
        "rem_ratio",
        "deep_ratio",
        "resting_hr",
        "steps",
        "hr_elevated",
        "fatigue_high",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    feats[keep].to_csv(OUT, index=False)
    print(f"Wrote {len(feats)} rows to {OUT}")


if __name__ == "__main__":
    main()
