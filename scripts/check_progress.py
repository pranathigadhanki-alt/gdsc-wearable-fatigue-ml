#!/usr/bin/env python3
"""Mentor validation — solutions pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mentor", action="store_true")
    args = parser.parse_args()
    if not args.mentor:
        from scripts.check_session import main as cli

        cli()
        return

    from solutions.data_loader import load_feature_table, load_person_baselines
    from solutions.models import FEATURE_COLUMNS, predict_recovery, train_model
    from solutions.counterfactuals import suggest_what_ifs
    from solutions.baselines import build_model_row

    df = load_feature_table(use_demo=True)
    baselines = load_person_baselines(use_demo=True)
    pipe = train_model(use_demo=True)
    pid = baselines["participant_id"].iloc[0]
    sig = ["sleep_duration", "heart_rate", "daily_steps", "physical_activity_level"]
    today = {c: float(baselines.iloc[0][c]) for c in sig}
    last = dict(today)
    row = build_model_row(pid, today, last, baselines)
    predict_recovery(row, pipe)
    suggest_what_ifs(pid, today, last, baselines, pipe, 0.5)
    print("Mentor OK:", len(df), "rows,", len(FEATURE_COLUMNS), "features")


if __name__ == "__main__":
    main()
