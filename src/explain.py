"""Session 7 — Why tab (today vs *your* baseline)."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline


@dataclass
class Reason:
    icon: str
    tone: str
    title: str
    detail: str


def explain_prediction(
    model_row: dict,
    baselines: pd.DataFrame,
    participant_id,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list[Reason], str]:
    raise NotImplementedError("Session 7 — see solutions/explain.py")
