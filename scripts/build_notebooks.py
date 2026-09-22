#!/usr/bin/env python3
"""Generate Colab-ready session notebooks."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

WEEKS = [
    (
        "week01_kickoff",
        "Session 1 — Kaggle, Colab, charter",
        [
            "Fill-in-the-blank project: you implement `src/` each session. Dataset: Kaggle Sleep Health and Lifestyle.",
            "from google.colab import drive\ndrive.mount('/content/drive')",
            "!git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git\n%cd gdsc-wearable-fatigue-ml\n!pip install -q -r requirements.txt",
            "# Kaggle API — see docs/KAGGLE_SETUP.md\n# !pip install -q kaggle\n# !kaggle datasets download -d uom190346a/sleep-health-and-lifestyle-dataset -p data/kaggle --unzip",
            "!python scripts/generate_demo_data.py",
            "import pandas as pd\nfrom src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)\ndf.head()",
            "**In session:** Implement `load_kaggle_raw` in `src/data_loader.py`, then load real CSV when ready.",
        ],
    ),
    (
        "week02_eda",
        "Session 2 — EDA on Kaggle columns",
        [
            "from src.data_loader import load_kaggle_raw, load_feature_table\n# raw = load_kaggle_raw()  # after Session 1\ndf = load_feature_table(use_demo=True)",
            "import seaborn as sns\nimport matplotlib.pyplot as plt\ndf.describe().T",
            "sns.scatterplot(data=df, x='stress_level', y='quality_of_sleep', hue='fatigue_high')",
            "**In session:** Notes in notebook — which columns predict fatigue?",
        ],
    ),
    (
        "week03_features",
        "Session 3 — Feature engineering",
        [
            "from src.features import build_features_from_kaggle, fatigue_label\nfrom src.data_loader import load_kaggle_raw",
            "# raw = load_kaggle_raw()\n# feats = build_features_from_kaggle(raw)\n# feats['fatigue_high'] = fatigue_label(feats)",
            "**In session:** Complete `src/features.py` and `load_feature_table` in `src/data_loader.py`.",
        ],
    ),
    (
        "week04_splits_and_metrics",
        "Session 4 — Splits & metrics",
        [
            "from sklearn.model_selection import GroupShuffleSplit\nfrom sklearn.dummy import DummyClassifier\nfrom src.data_loader import load_feature_table, participant_groups\nfrom src.models import FEATURE_COLUMNS",
            "df = load_feature_table(use_demo=True)\n# X, y, groups, split, baseline — after TODOs done",
            "from src.metrics_utils import evaluate_classifier, plot_confusion_matrix",
        ],
    ),
    (
        "week05_model_compare",
        "Session 5 — Logistic vs Random Forest",
        [
            "from src.models import build_logistic_pipeline, build_rf_pipeline, FEATURE_COLUMNS",
            "**In session:** Implement both pipelines in `src/models.py` and compare metrics.",
        ],
    ),
    (
        "week06_tuning_and_imbalance",
        "Session 6 — Tuning & imbalance",
        [
            "from sklearn.model_selection import GridSearchCV\nfrom imblearn.over_sampling import SMOTE",
        ],
    ),
    (
        "week07_model_and_streamlit",
        "Session 7 — Save model & Streamlit",
        [
            "from src.models import train_model, save_model\n# pipe = train_model(use_demo=True); save_model(pipe)",
            "# !streamlit run app/streamlit_app.py",
        ],
    ),
    (
        "week08_showcase",
        "Session 8 — Showcase",
        [
            "Slides: Kaggle citation, label rule, confusion matrix, live Streamlit, limitations.",
        ],
    ),
    (
        "optional_wesad_stress",
        "Optional — WESAD extension",
        ["For teams finishing early — wearable lab stress dataset."],
    ),
]


def cell(source: str, cell_type: str = "code") -> dict:
    if cell_type == "markdown":
        return {"cell_type": "markdown", "metadata": {}, "source": [source if source.endswith("\n") else source + "\n"]}
    lines = source.split("\n")
    src = [line + "\n" for line in lines[:-1]]
    if lines[-1]:
        src.append(lines[-1] + "\n")
    elif not src:
        src = ["\n"]
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None}


def build_notebook(title: str, parts: list[str]) -> dict:
    cells = [cell(f"# {title}\n", "markdown")]
    for part in parts:
        if part.startswith("**") or part.startswith("#") or part.startswith("Slides") or part.startswith("Fill"):
            cells.append(cell(part, "markdown"))
        elif part.startswith("For teams"):
            cells.append(cell(part, "markdown"))
        else:
            cells.append(cell(part, "code"))
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "colab": {"provenance": []},
        },
        "cells": cells,
    }


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for filename, title, parts in WEEKS:
        path = NOTEBOOKS / f"{filename}.ipynb"
        path.write_text(json.dumps(build_notebook(title, parts), indent=1))
        print("Wrote", path)


if __name__ == "__main__":
    main()
