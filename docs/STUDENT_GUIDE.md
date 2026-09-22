# Student workbook

## One path to the preview

1. Read **[BUILD_PATH.md](BUILD_PATH.md)** — session-by-session through the same UI as the mentor demo.
2. Each session: open **`weeks/weekNN/README.md`** + **`notebooks/weekNN_*.ipynb`**.
3. Fill in **`src/`** (search `TODO` and `NotImplementedError`).
4. After each session: `python scripts/check_session.py`

## What you do NOT rebuild

The Streamlit **layout** is already in the repo:

- `app/ui_theme.py` — styling  
- `app/dashboard.py` — tabs, gauge, presets, explanation panels  
- `app/streamlit_app.py` — connects **your** `src/` when Session 7 is complete  

Until Session 7, `streamlit_app.py` shows a **progress checklist**.

## Files by session

| Session | `src/` |
|---------|--------|
| 1 | `data_loader.load_kaggle_raw` |
| 3 | `features.py`, `load_feature_table` |
| 4 | `metrics_utils.py`, `participant_groups` |
| 5 | `build_*_pipeline` |
| 7 | `train_model`, `predict_recovery`, `baselines.build_model_row`, `explain.py`, `counterfactuals.py` |

## Data

[KAGGLE_SETUP.md](KAGGLE_SETUP.md) — practice with `data/sample_demo.csv` first.

## Mentor key

`solutions/` — do not copy until showcase unless your mentor says so.
