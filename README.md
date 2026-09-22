# GDSC — Wearable fatigue ML (fill-in-the-blank)

Eight in-room sessions building a **stress/fatigue classifier** from the **[Kaggle Sleep Health and Lifestyle dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)**, plus a **Streamlit** demo for showcase.

**Students:** implement TODOs in **`src/`** — see [docs/STUDENT_GUIDE.md](docs/STUDENT_GUIDE.md).  
**Mentor:** answer key in **`solutions/`** — [docs/MENTOR.md](docs/MENTOR.md).

**Repo:** https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml

## Quick start

```bash
git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git
cd gdsc-wearable-fatigue-ml
pip install -r requirements.txt
python scripts/generate_demo_data.py
```

1. [docs/KAGGLE_SETUP.md](docs/KAGGLE_SETUP.md) — download CSV to `data/kaggle/`
2. [docs/CURRICULUM.md](docs/CURRICULUM.md) — session plan
3. Open `notebooks/week01_kickoff.ipynb` in Colab

## Project layout

| Path | Role |
|------|------|
| `src/` | **Your code** (fill in the blanks) |
| `solutions/` | Mentor reference — don’t peek until showcase |
| `notebooks/` | Session walkthroughs |
| `app/streamlit_app.py` | Demo UI (Session 7+) |
| `docs/STUDENT_GUIDE.md` | TODO map by session |

## Sessions at a glance

| # | Topic | `src/` focus |
|---|--------|----------------|
| 1 | Kaggle + Colab | `load_kaggle_raw` |
| 2 | EDA | notebook |
| 3 | Features + labels | `features.py`, `load_feature_table` |
| 4 | Metrics + splits | `metrics_utils.py`, `participant_groups` |
| 5 | Logistic vs RF | `models.py` pipelines |
| 6 | Tuning / imbalance | notebook + models |
| 7 | joblib + Streamlit | `train_model`, `predict_fatigue`, app |
| 8 | Showcase | Slides + ethics |

## License

MIT — [LICENSE](LICENSE). Follow [Kaggle dataset terms](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) for the CSV.
