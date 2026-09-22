#!/usr/bin/env python3
"""Create weeks/weekNN/README.md — tied to BUILD_PATH.md and the preview UI."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SESSIONS = [
    (
        1,
        "Kickoff & Kaggle",
        "week01_kickoff.ipynb",
        "src/data_loader.py",
        ["Implement `load_kaggle_raw`", "Merge team charter", "Run demo: `python scripts/generate_demo_data.py`"],
    ),
    (
        2,
        "EDA",
        "week02_eda.ipynb",
        "notebook only",
        ["3 plots + bullets in notebook", "Map Kaggle columns → model inputs"],
    ),
    (
        3,
        "Features & labels",
        "week03_features.ipynb",
        "src/features.py, src/data_loader.py",
        ["`build_features_from_kaggle`", "`fatigue_label`", "`load_feature_table(use_demo=True)`"],
    ),
    (
        4,
        "Splits & metrics",
        "week04_splits_and_metrics.ipynb",
        "src/metrics_utils.py, participant_groups",
        ["Group split by person", "Baseline + confusion matrix", "`evaluate_classifier`"],
    ),
    (
        5,
        "Model compare",
        "week05_model_compare.ipynb",
        "src/models.py",
        ["`build_logistic_pipeline`", "`build_rf_pipeline`", "Compare in notebook"],
    ),
    (
        6,
        "Tuning",
        "week06_tuning_and_imbalance.ipynb",
        "notebook (+ optional best_params.json)",
        ["GridSearchCV", "Discuss class imbalance"],
    ),
    (
        7,
        "Full preview app",
        "week07_model_and_streamlit.ipynb",
        "src/models.py, src/explain.py",
        [
            "`train_model`, `predict_fatigue`, `explain_prediction`",
            "`PYTHONPATH=. streamlit run app/streamlit_app.py` → same UI as mentor preview",
            "`python scripts/check_session.py` → Dashboard ready",
        ],
    ),
    (
        8,
        "Showcase",
        "week08_showcase.ipynb",
        "Google Slides",
        ["Dry-run demo", "Ethics slide", "Kaggle citation"],
    ),
]

TEMPLATE = """# Session {n}: {title}

**Notebook:** [`notebooks/{notebook}`](../../notebooks/{notebook})  
**Build guide:** [docs/BUILD_PATH.md](../../docs/BUILD_PATH.md) (Session {n})  
**Check progress:** `python scripts/check_session.py`

## Edit this session

**Primary file(s):** `{files}`

## Done when

{done_list}

## Flow (~90–120 min)

1. Mentor concept (5–15 min)
2. Work through the notebook in Colab
3. Implement the `src/` TODOs for this session
4. PR before you leave; run `check_session.py`

## Preview alignment

The final app (`app/streamlit_app.py`) uses `app/dashboard.py` — **you do not rewrite the UI**. Each session adds backend logic until Session 7 unlocks the full colorful dashboard (gauge, explanations, presets).
"""


def main() -> None:
    for n, title, notebook, files, done in SESSIONS:
        folder = ROOT / "weeks" / f"week{n:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        done_md = "\n".join(f"- [ ] {d}" for d in done)
        (folder / "README.md").write_text(
            TEMPLATE.format(n=n, title=title, notebook=notebook, files=files, done_list=done_md)
        )
    print("Session READMEs updated.")


if __name__ == "__main__":
    main()
