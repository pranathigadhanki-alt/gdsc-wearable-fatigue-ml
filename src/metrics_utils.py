"""
Evaluation helpers — Session 4.

Used for baseline vs model comparison and confusion matrix slides.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, roc_auc_score


def evaluate_classifier(y_true, y_pred, y_proba=None) -> dict[str, Any]:
    """
    Session 4 — Return accuracy, precision/recall/F1 for positive class, optional ROC-AUC.

    Hint: classification_report(..., output_dict=True) and read key "1" for positive class.
    """
    # TODO: report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    # TODO: build dict with accuracy, precision_pos, recall_pos, f1_pos
    # TODO: if y_proba and binary labels: out["roc_auc"] = roc_auc_score(y_true, y_proba)
    raise NotImplementedError("Complete evaluate_classifier in Session 4.")


def plot_confusion_matrix(y_true, y_pred, labels=("Low fatigue", "High fatigue")):
    """Session 4 — Matplotlib figure with ConfusionMatrixDisplay."""
    fig, ax = plt.subplots(figsize=(4, 4))
    # TODO: ConfusionMatrixDisplay.from_predictions(..., ax=ax)
    ax.set_title("Confusion matrix — fill in ConfusionMatrixDisplay")
    fig.tight_layout()
    return fig
