"""
Session 7+ — Plain-language explanations for Streamlit.

Mirror the logic in `solutions/explain.py` once your model works.
"""

from __future__ import annotations

import pandas as pd
from sklearn.pipeline import Pipeline


def explain_prediction(
    row: dict,
    reference: pd.DataFrame,
    pipe: Pipeline,
    label: int,
    proba: float,
) -> tuple[list, str]:
    """
    TODO Session 7:
      1. List 2–4 reasons (sleep quality, stress proxy, heart rate, sleep hours).
      2. Optionally use RandomForest feature_importances_.
      3. Return (list of reason dicts or dataclass, summary paragraph string).

    See `solutions/explain.py` for mentor reference.
    """
    raise NotImplementedError("Complete explain_prediction in Session 7.")
