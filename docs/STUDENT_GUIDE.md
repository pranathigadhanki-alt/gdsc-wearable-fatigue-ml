# Student workbook guide

This repo is a **fill-in-the-blank** project. You implement ML in **`src/`** session by session; notebooks walk you through each step.

## Where to write code

| Session | File | What you implement |
|---------|------|-------------------|
| 1 | `src/data_loader.py` | `load_kaggle_raw` |
| 3 | `src/features.py`, `src/data_loader.py` | Features + `load_feature_table` |
| 4 | `src/metrics_utils.py`, `src/data_loader.py` | Metrics + `participant_groups` |
| 5–7 | `src/models.py` | Pipelines, train, predict |
| 7–8 | `app/streamlit_app.py` | UI tweaks (optional) |

Search for **`TODO`** and **`NotImplementedError`** in `src/`.

## Data

1. Practice: `data/sample_demo.csv` (already in repo).
2. Real: download Kaggle CSV — [KAGGLE_SETUP.md](KAGGLE_SETUP.md).

## How to check your work

- Notebook for that session runs without error.
- `pytest` (optional) — mentor may run `scripts/check_progress.py`.
- Compare your logic to the team charter label rules (Session 1).

## Rules

- Do not commit `data/kaggle/*.csv`.
- Open PRs to `main` each session.
- Do not open the `solutions/` folder until after the showcase (mentor reference).
