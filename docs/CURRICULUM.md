# 8-session GDSC curriculum

Each session adds **`src/`** code until the **mentee Streamlit app** matches the mentor preview. Master checklist: **[BUILD_PATH.md](BUILD_PATH.md)**.

**Stack:** Colab + Drive + this repo · **Data:** [KAGGLE_SETUP.md](KAGGLE_SETUP.md)

---

## Session 1 — Kaggle + `load_kaggle_raw`

Charter, clone repo, demo CSV, implement raw CSV loader.  
→ [weeks/week01/README.md](../weeks/week01/README.md)

## Session 2 — EDA

Notebook plots; map columns for features. No `src/` required.

## Session 3 — Features + labels

`build_features_from_kaggle`, lags, `better_night_tomorrow_label`, disorder cohort, `load_feature_table`.

## Session 4 — Splits & metrics

`participant_groups`, `evaluate_classifier`, baseline model in notebook.

## Session 5 — Logistic vs Random Forest

Implement pipelines; compare metrics.

## Session 6 — Tuning & imbalance

GridSearchCV; optional SMOTE discussion.

## Session 7 — Full preview app

`train_model`, `predict_recovery`, `build_model_row`, `explain_prediction`, `suggest_what_ifs` → **`streamlit run app/streamlit_app.py`** (recovery gauge, last night + tonight, what-if).

## Session 8 — Showcase

Google Slides + live demo + ethics.

---

**Progress command:** `python scripts/check_session.py`  
**Mentor demo (complete code):** `PYTHONPATH=. streamlit run app/mentor_preview.py`

7-session variant: merge 2→1 or 8→7 per [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md).
