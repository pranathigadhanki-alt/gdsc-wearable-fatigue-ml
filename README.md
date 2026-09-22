# StrainScope — GDSC wearable ML (week-by-week)

**Elevator pitch:** We don’t ask how stressed you feel. We use **watch-like signals** (sleep, heart rate, steps, activity) and **your personal baseline** to estimate **next-day strain** — then show **what changes** (more sleep, more steps) move the needle most.

| | |
|--|--|
| **Mentees** | [docs/BUILD_PATH.md](docs/BUILD_PATH.md) → fill `src/` each session |
| **Mentor demo** | `PYTHONPATH=. streamlit run app/mentor_preview.py` |
| **Data** | [Kaggle Sleep Health & Lifestyle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) |
| **Repo** | https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml |

```bash
git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git
cd gdsc-wearable-fatigue-ml
pip install -r requirements.txt
python scripts/generate_demo_data.py
PYTHONPATH=. streamlit run app/mentor_preview.py
```

## Why this needs ML

- Labels come from **hidden** self-report in training (stress/sleep quality) — **not** from sliders at demo time.
- The model learns when **objective** patterns + **deviation from your baseline** predict strain better than one-size-fits-all rules.
- **What-if** scenarios re-run the model — not hand-waved advice.

## Sessions → product

| Session | Build | Unlocks |
|---------|--------|---------|
| 1–2 | Kaggle + EDA | Data story |
| 3 | Baselines + deltas + labels | Personal «vs you» |
| 4–6 | Metrics + sklearn | Honest evaluation |
| 7 | Model + explain + what-if | **Full StrainScope UI** |
| 8 | Slides + live demo | Showcase |

`python scripts/check_session.py` · MIT [LICENSE](LICENSE)
