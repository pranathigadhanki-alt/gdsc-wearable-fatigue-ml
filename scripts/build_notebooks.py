#!/usr/bin/env python3
"""Generate Colab-ready notebooks (8 GDSC sessions)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

WEEKS = [
    (
        "week01_kickoff",
        "Session 1 — Kickoff: problem, Colab, charter",
        [
            "Define fatigue prediction from wearables. All work stays in this repo — no outside assignments.",
            "from google.colab import drive\ndrive.mount('/content/drive')",
            "!git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git\n%cd gdsc-wearable-fatigue-ml\n!pip install -q -r requirements.txt",
            "!python scripts/generate_demo_data.py",
            "from src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)\ndf.head()",
            "df['fatigue_high'].value_counts(normalize=True).plot(kind='bar', title='Label balance')",
            "**Before end of session:** PR with completed `templates/team_charter.md` (label rules + success metric).",
        ],
    ),
    (
        "week02_eda",
        "Session 2 — Exploratory data analysis",
        [
            "import seaborn as sns\nimport matplotlib.pyplot as plt\nfrom src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)",
            "df.describe().T",
            "sns.pairplot(df, hue='fatigue_high', vars=['sleep_efficiency','resting_hr','steps'])",
            "df.corr(numeric_only=True)",
            "**Session output:** Keep 3 plots + bullet insights in this notebook; commit to repo.",
        ],
    ),
    (
        "week03_features",
        "Session 3 — Feature engineering",
        [
            "from src.features import nightly_sleep_features, rule_based_fatigue_label",
            "from src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)\ndf.head()",
            "# Map PMData columns here when Drive data is ready",
            "**Session output:** Update `src/features.py` and note Drive path to features_v1.csv.",
        ],
    ),
    (
        "week04_splits_and_metrics",
        "Session 4 — Splits, leakage, metrics",
        [
            "from sklearn.model_selection import GroupShuffleSplit\nfrom sklearn.dummy import DummyClassifier\nfrom src.data_loader import load_feature_table, participant_day_groups\nfrom src.models import FEATURE_COLUMNS",
            "df = load_feature_table(use_demo=True)\nX, y = df[FEATURE_COLUMNS], df['fatigue_high']\ngroups = participant_day_groups(df)\nsplit = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)\ntrain_idx, test_idx = next(split.split(X, y, groups=groups))",
            "from src.metrics_utils import evaluate_classifier, plot_confusion_matrix",
            "**Session output:** Record the team's primary metric in team_charter.md.",
        ],
    ),
    (
        "week05_model_compare",
        "Session 5 — Logistic regression vs Random Forest",
        [
            "from src.models import build_logistic_pipeline, build_rf_pipeline, FEATURE_COLUMNS\nfrom src.data_loader import load_feature_table\ndf = load_feature_table(use_demo=True)\nX, y = df[FEATURE_COLUMNS], df['fatigue_high']",
            "log_reg = build_logistic_pipeline()\nrf = build_rf_pipeline()\n# fit on train_idx from session 4; compare metrics",
            "**Session output:** Short comparison table in markdown below.",
        ],
    ),
    (
        "week06_tuning_and_imbalance",
        "Session 6 — Cross-validation, tuning, imbalance",
        [
            "from sklearn.model_selection import GridSearchCV, cross_val_score\nparam_grid = {'clf__n_estimators': [100, 200], 'clf__max_depth': [None, 5, 10]}",
            "from imblearn.over_sampling import SMOTE\n# Discuss whether SMOTE fits grouped wearable data",
            "**Session output:** Save best_params.json; note recall/precision tradeoff in notebook.",
        ],
    ),
    (
        "week07_model_and_streamlit",
        "Session 7 — Final model + Streamlit",
        [
            "from src.models import save_model, train_demo_model\npipe = train_demo_model(use_demo=True)\nsave_model(pipe)",
            "# Locally: streamlit run app/streamlit_app.py",
            "**Session output:** PR that connects app sliders to your FEATURE_COLUMNS.",
        ],
    ),
    (
        "week08_showcase",
        "Session 8 — Showcase rehearsal",
        [
            "Checklist: limitations slide, PMData/WESAD citations, live Streamlit, not medical advice.",
            "Google Slides link (team): paste URL in your repo README.",
        ],
    ),
    (
        "optional_wesad_stress",
        "Optional — WESAD stress extension",
        [
            "After PMData pipeline ships — load WESAD and compare stress vs fatigue labels.",
        ],
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
        if part.startswith("**") or part.startswith("#") or part.startswith("Checklist") or part.startswith("Google"):
            cells.append(cell(part, "markdown"))
        elif part.startswith("Define") or part.startswith("After"):
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
    keep = {f"{name}.ipynb" for name, _, _ in WEEKS}
    for old in NOTEBOOKS.glob("week*.ipynb"):
        if old.name not in keep and old.name != "optional_wesad_stress.ipynb":
            old.unlink()
            print("Removed", old)
    for filename, title, parts in WEEKS:
        path = NOTEBOOKS / f"{filename}.ipynb"
        path.write_text(json.dumps(build_notebook(title, parts), indent=1))
        print("Wrote", path)


if __name__ == "__main__":
    main()
