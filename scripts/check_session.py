#!/usr/bin/env python3
"""CLI wrapper for app/progress.py — run after each session."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.progress import ready_for_dashboard, session_status


def main() -> None:
    for line in session_status():
        print(line.replace("**", ""))
    print()
    if ready_for_dashboard():
        print("Dashboard ready: PYTHONPATH=. streamlit run app/streamlit_app.py")
    else:
        print("Keep going — follow docs/BUILD_PATH.md for this session.")


if __name__ == "__main__":
    main()
