# Build path — week by week to the full preview

The **mentor preview** and **mentee app** use the same UI (`app/dashboard.py`). Mentees implement **`src/`** step by step; when Session 7 checks pass, `streamlit run app/streamlit_app.py` looks identical to the preview.

Check progress anytime:

```bash
python scripts/check_session.py
```

| Session | You implement | Preview feature unlocked |
|---------|----------------|-------------------------|
| **1** | `load_kaggle_raw` in `src/data_loader.py` | Load real Kaggle CSV in Colab |
| **2** | Notebook EDA only | Understand columns for features |
| **3** | `build_features_from_kaggle`, `fatigue_label`, `load_feature_table` | Feature table + labels |
| **4** | `participant_groups`, `evaluate_classifier` | Metrics + split story for slides |
| **5** | `build_logistic_pipeline`, `build_rf_pipeline` | Model comparison in notebook |
| **6** | Tuning in `notebooks/week06_*.ipynb` | Better scores (optional JSON params) |
| **7** | `train_model`, `predict_fatigue`, `explain_prediction` | **Full dashboard** (gauge, tabs, explanations) |
| **8** | Slides + rehearsal | Same app — showcase ready |

---

## Session 1 — Data access

**Files:** `src/data_loader.py` → `load_kaggle_raw`

1. Download CSV → [KAGGLE_SETUP.md](KAGGLE_SETUP.md)
2. Implement `load_kaggle_raw` (read CSV, clear error if missing)
3. Run `notebooks/week01_kickoff.ipynb`
4. PR: team charter + `load_kaggle_raw`

**Test:** `python scripts/check_session.py` shows Session 1 ✅

---

## Session 2 — EDA

**Files:** notebook only (no `src/` required)

1. `load_feature_table(use_demo=True)` or raw Kaggle
2. Three plots: stress vs sleep quality, heart rate distribution, fatigue balance
3. Bullet notes: which columns go into the model?

**Test:** Notebook runs; informs Session 3 renames

---

## Session 3 — Features

**Files:** `src/features.py`, finish `load_feature_table` in `src/data_loader.py`

1. Copy rename map from docstrings (Kaggle → snake_case)
2. Add `gender_male`, `stress_x_poor_sleep` (computed from stress + sleep quality — the app calculates this for users; see `app/input_helpers.py`)
3. Implement `fatigue_label` per team charter
4. `load_feature_table`: demo CSV → later Kaggle path

**Test:** Session 3 checks ✅; `load_feature_table(use_demo=True)` returns `fatigue_high`

---

## Session 4 — Metrics & splits

**Files:** `src/metrics_utils.py`, `participant_groups` in `src/data_loader.py`

1. Group split by `participant_id` in notebook
2. Dummy classifier baseline
3. `evaluate_classifier` + confusion matrix plot

**Test:** Session 4 checks ✅

---

## Session 5 — Two models

**Files:** `src/models.py` — pipelines only (not train yet)

1. Logistic + StandardScaler
2. Random Forest
3. Notebook: compare validation F1/recall

**Test:** Session 5 checks ✅

---

## Session 6 — Tuning

**Files:** notebook + optional `models/best_params.json`

1. `GridSearchCV` on RF or logistic
2. Discuss imbalance (`class_weight`, optional SMOTE)

---

## Session 7 — Ship the preview

**Files:** `src/models.py` (`train_model`, `predict_fatigue`), `src/explain.py`, use existing `app/streamlit_app.py`

1. Implement training on group split (see `solutions/models.py` if stuck — mentor only)
2. Implement `explain_prediction` — rule reasons + summary (see `solutions/explain.py`)
3. Add `"stress_x_poor_sleep"` to `FEATURE_COLUMNS`
4. Run:

```bash
PYTHONPATH=. streamlit run app/streamlit_app.py
```

You should see: **presets, gauge, “Why this score?”, bar chart** — same as mentor preview.

**Test:** `python scripts/check_session.py` prints “Dashboard ready”

---

## Session 8 — Showcase

1. Google Slides — [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)
2. Live demo from `streamlit_app.py`
3. Ethics disclaimer

---

## UI code (already in repo)

Mentees **do not** rebuild UI from scratch:

- `app/ui_theme.py` — colors/fonts
- `app/dashboard.py` — tabs, gauge, presets
- `app/streamlit_app.py` — wires **your** `src/` into that UI

Optional: read `app/dashboard.py` to see how explanations connect to `explain_prediction`.
