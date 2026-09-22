#!/usr/bin/env python3
"""Quick sanity check — students use after each session; mentor uses --mentor."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mentor", action="store_true", help="Test solutions/ implementations")
    args = parser.parse_args()

    if args.mentor:
        from solutions import data_loader as dl
        from solutions import models

        df = dl.load_feature_table(use_demo=True)
        assert "fatigue_high" in df.columns
        pipe = models.train_model(use_demo=True)
        row = df[models.FEATURE_COLUMNS].iloc[0].to_dict()
        models.predict_fatigue(row, pipe)
        print("Mentor check OK:", len(df), "rows,", len(models.FEATURE_COLUMNS), "features")
        return

    import src.data_loader as dl

    try:
        df = dl.load_feature_table(use_demo=True)
        print("load_feature_table OK:", df.shape)
    except NotImplementedError as e:
        print("Still in progress:", e)


if __name__ == "__main__":
    main()
