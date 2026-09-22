#!/usr/bin/env python3
"""Generate Colab session notebooks aligned with BUILD_PATH.md."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

SETUP = """!git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git
%cd gdsc-wearable-fatigue-ml
!pip install -q -r requirements.txt
!python scripts/generate_demo_data.py"""

WEEKS = [
    (
        "week01_kickoff",
        "Session 1 — Kaggle + load_kaggle_raw",
        [
            "## Goal\nImplement `src/data_loader.load_kaggle_raw` so your team can read the Kaggle CSV.\n\nSee **docs/BUILD_PATH.md** Session 1.",
            "from google.colab import drive\ndrive.mount('/content/drive')",
            SETUP,
            "# Download Kaggle CSV to data/kaggle/ — see docs/KAGGLE_SETUP.md",
            "import pandas as pd\nfrom src.data_loader import load_feature_table\nload_feature_table(use_demo=True).head()",
            "from src.kaggle_schema import KAGGLE_FILENAME\nprint('Expect file:', KAGGLE_FILENAME)",
            "## PR checklist\n- [ ] team_charter.md\n- [ ] load_kaggle_raw implemented\n- [ ] python scripts/check_session.py",
        ],
    ),
    (
        "week02_eda",
        "Session 2 — EDA",
        [
            "## Goal\nThree figures + bullets — no new `src/` required.\n\nInforms Session 3 features.",
            SETUP,
            "import seaborn as sns\nimport matplotlib.pyplot as plt\nfrom src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)",
            "df.describe().T",
            "sns.countplot(data=df, x='sleep_disorder')",
            "df['better_night_tomorrow'].value_counts().plot(kind='bar', title='Recovery label balance')",
            "## Write in this notebook\n1. Insomnia vs sleep apnea — different patterns?\n2. Do lags help explain tomorrow?\n3. Charter label still OK?",
        ],
    ),
    (
        "week03_features",
        "Session 3 — Features",
        [
            "## Goal\nComplete `src/features.py` + `load_feature_table`.\n\nAfter this, check_session Session 3 ✅",
            SETUP,
            "from src.features import build_features_from_kaggle, better_night_tomorrow_label, add_lag_features",
            "from src.data_loader import load_kaggle_raw, load_feature_table",
            "# raw = load_kaggle_raw()  # when CSV on Drive\n# feats = build_features_from_kaggle(raw)\n# feats = add_lag_features(feats)\n# feats['better_night_tomorrow'] = better_night_tomorrow_label(feats)",
            "load_feature_table(use_demo=True).head()",
        ],
    ),
    (
        "week04_splits_and_metrics",
        "Session 4 — Splits & metrics",
        [
            "## Goal\n`participant_groups`, `evaluate_classifier`, baseline in notebook.",
            SETUP,
            "from sklearn.model_selection import GroupShuffleSplit\nfrom sklearn.dummy import DummyClassifier\nfrom src.data_loader import load_feature_table, participant_groups\nfrom src.models import FEATURE_COLUMNS\nfrom src.metrics_utils import evaluate_classifier, plot_confusion_matrix",
            "df = load_feature_table(use_demo=True)\nX, y = df[FEATURE_COLUMNS], df['better_night_tomorrow']\ngroups = participant_groups(df)",
            "# TODO: split, fit DummyClassifier, evaluate_classifier, plot_confusion_matrix",
        ],
    ),
    (
        "week05_model_compare",
        "Session 5 — Logistic vs RF",
        [
            "## Goal\nImplement pipelines in `src/models.py`, compare in notebook.",
            SETUP,
            "from src.models import build_logistic_pipeline, build_rf_pipeline, FEATURE_COLUMNS\nfrom src.data_loader import load_feature_table",
            "# Train both on train_idx; table of precision/recall/F1",
        ],
    ),
    (
        "week06_tuning_and_imbalance",
        "Session 6 — Tuning",
        [
            "## Goal\nGridSearchCV + imbalance discussion.",
            SETUP,
            "from sklearn.model_selection import GridSearchCV",
            "# Optional: imblearn SMOTE — when is it valid for grouped data?",
        ],
    ),
    (
        "week07_model_and_streamlit",
        "Session 7 — Unlock the preview",
        [
            "## Goal\nFinish `train_model`, `predict_recovery`, `build_model_row`, `src/explain.py`, `src/counterfactuals.py`.\n\nThen:\n`PYTHONPATH=. streamlit run app/streamlit_app.py`\n\nSame UI as mentor preview.",
            SETUP,
            "from src.models import train_model, save_model, predict_recovery\nfrom src.explain import explain_prediction",
            "# pipe = train_model(use_demo=True); save_model(pipe)",
            "!python scripts/check_session.py",
            "# Local: !pip install -q streamlit plotly && PYTHONPATH=. streamlit run app/streamlit_app.py",
        ],
    ),
    (
        "week08_showcase",
        "Session 8 — Showcase",
        [
            "## Goal\nSlides + live demo from **your** streamlit_app.py\n\nSee docs/PRESENTATION_GUIDE.md",
            "- Kaggle citation\n- Disorder cohort + recovery label rule\n- Confusion matrix slide\n- Live gauge + Get better tomorrow tab\n- Not a sleep study / not medical advice",
        ],
    ),
    (
        "optional_wesad_stress",
        "Optional — WESAD",
        ["Extension for teams finishing early."],
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
        if part.startswith("##") or part.startswith("- ") or part.startswith("Extension"):
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
