"""Evaluation helpers for classification (Week 5+)."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    roc_auc_score,
)


def evaluate_classifier(y_true, y_pred, y_proba=None) -> dict[str, Any]:
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    out: dict[str, Any] = {
        "accuracy": report["accuracy"],
        "precision_pos": report.get("1", {}).get("precision", 0.0),
        "recall_pos": report.get("1", {}).get("recall", 0.0),
        "f1_pos": report.get("1", {}).get("f1-score", 0.0),
    }
    if y_proba is not None and len(np.unique(y_true)) == 2:
        out["roc_auc"] = roc_auc_score(y_true, y_proba)
    return out


def plot_confusion_matrix(y_true, y_pred, labels=("Low fatigue", "High fatigue")):
    fig, ax = plt.subplots(figsize=(4, 4))
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, display_labels=labels, ax=ax)
    ax.set_title("Confusion matrix")
    fig.tight_layout()
    return fig
