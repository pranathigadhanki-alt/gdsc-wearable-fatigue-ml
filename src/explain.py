"""
Session 7 — Plain-language explanations (powers the «Why this score?» tab).

When done, matches behavior in `solutions/explain.py`.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline


@dataclass
class Reason:
    icon: str
    tone: str  # risk | ok | neutral
    title: str
    detail: str


def rule_reasons(row: dict, reference: pd.DataFrame) -> list[Reason]:
    """Session 7a — Sleep quality, stress×sleep, heart rate, sleep hours (see BUILD_PATH.md)."""
    # TODO: append Reason(...) objects when thresholds crossed
    raise NotImplementedError("Session 7: implement rule_reasons")


def model_reasons(row: dict, pipe: Pipeline) -> list[Reason]:
    """Optional — prefer plain `rule_reasons` only (see solutions/explain.py)."""
    del row, pipe
    return []


def build_summary(label: int, proba: float, reasons: list[Reason]) -> str:
    """Session 7c — One paragraph for the Summary section."""
    # TODO: lead sentence with proba; mention top risk reasons
    raise NotImplementedError("Session 7: implement build_summary")


def explain_prediction(
    row: dict,
    reference: pd.DataFrame,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list[Reason], str]:
    """Session 7 — Called from app/dashboard.py on every prediction."""
    # TODO: rules = rule_reasons(...); model = model_reasons(...); merge; summary = build_summary(...)
    raise NotImplementedError("Session 7: wire explain_prediction")
