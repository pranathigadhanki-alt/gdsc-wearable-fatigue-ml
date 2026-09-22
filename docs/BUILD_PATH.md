# Build path — StrainScope

**Judges narrative:** *We don’t ask how stressed you feel. We use watch-like signals to estimate next-day strain, compare you to your own baseline, and show what change (sleep, steps) moves the needle most.*

Mentees implement **`src/`**; UI is already in **`app/dashboard.py`**. Mentor runs **`app/mentor_preview.py`**.

```bash
python scripts/check_session.py
```

---

## Session 1 — Kaggle + charter

- Implement `load_kaggle_raw`
- Charter: define **strain** and why we **hide** survey questions at inference
- Notebook: `week01_kickoff.ipynb`

---

## Session 2 — EDA

- Explore sleep, HR, steps **per person**
- Note: same person varies night to night → baselines matter

---

## Session 3 — Baselines + labels (core idea)

**Files:** `src/baselines.py`, `src/features.py`, `src/data_loader.py`

1. `compute_person_baselines` — median watch signals per `participant_id`
2. `add_baseline_deltas` — `sleep_duration_delta`, etc.
3. `strain_label` — training only: `(stress ≥ 7) | (quality ≤ 5)` from Kaggle
4. `load_feature_table`, `load_person_baselines`

**No stress/quality sliders in the final app.**

---

## Session 4 — Splits & metrics

- Split by **person** (GroupShuffleSplit)
- Compare **rule baseline** (e.g. sleep delta only) vs upcoming ML on test set

---

## Session 5–6 — Models & tuning

- Features: `FEATURE_COLUMNS` in `src/models.py` (8 watch + delta columns)
- Logistic vs Random Forest; optional GridSearch

---

## Session 7 — Ship StrainScope

- `train_model`, `predict_strain`
- `src/explain.py` — today vs **your** baseline copy
- `src/counterfactuals.py` — what-if scenarios
- Run: `PYTHONPATH=. streamlit run app/streamlit_app.py`

---

## Session 8 — Showcase

- Live demo: pick person → bad day preset → **What moves the needle?** tab
- Slide: rules vs ML on held-out people
- Ethics: not medical advice; labels from self-report in training only

---

## Slide bullets

1. Problem: strain before you feel it — from the watch, not a survey  
2. Personal baseline vs population averages  
3. ML beats simple rules on held-out **people** (show metric)  
4. What-if: +1h sleep → −X pp strain  
5. Limitations & future (real Apple Health stream)
