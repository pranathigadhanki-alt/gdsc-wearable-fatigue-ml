# Build path — RecoveryScope

**Label:** `better_night_tomorrow` — next night’s sleep quality rises OR sleep duration increases (training only; uses Kaggle columns students never slider in the app).

**Cohort:** rows where `sleep_disorder` is **Insomnia** or **Sleep Apnea**.

**Features:** tonight’s watch signals + **deltas vs personal baseline** + **lag1_** (last night) + disorder flags.

---

| Session | Implement | Outcome |
|---------|-------------|---------|
| 1 | `load_kaggle_raw` | CSV on Drive |
| 2 | EDA by disorder | Plots in notebook |
| 3 | `add_lag_features`, `better_night_tomorrow_label`, `prepare_training_frame`, baselines | `sample_demo.csv` |
| 4 | Splits by person; rules vs ML slide | Metrics |
| 5–6 | Pipelines + tuning | RF/logistic |
| 7 | `predict_recovery`, explain, counterfactuals | Full **RecoveryScope** UI |
| 8 | Slides + demo | Showcase |

## Session 3 detail

1. Rename Kaggle columns; keep `sleep_disorder`.
2. Sort by person; `lag1_sleep_duration`, etc.
3. Label from **shift(-1)** on quality & sleep duration.
4. Filter to insomnia/apnea; drop rows without lag/label.

## Session 7

`PYTHONPATH=. streamlit run app/streamlit_app.py`

Mentor reference: `solutions/` only.

## Disclaimer (every showcase)

Educational tool on public data — **not** diagnosis, **not** CPAP/prescription advice.
