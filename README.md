# RecoveryScope — GDSC sleep disorder recovery ML

**Judges narrative:** We focus on people with **insomnia or sleep apnea** in public sleep data. From **watch-like signals**, **personal baselines**, and **last night’s history**, we estimate the chance of a **better night tomorrow**, then show which **sleep and activity changes** most improve that chance — **not** replacing a sleep study or doctor.

| | |
|--|--|
| **Mentees** | [docs/BUILD_PATH.md](docs/BUILD_PATH.md) |
| **Mentor demo** | `PYTHONPATH=. streamlit run app/mentor_preview.py` |
| **Data** | [Kaggle Sleep Health & Lifestyle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) |
| **Repo** | https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml |

```bash
pip install -r requirements.txt
python scripts/generate_demo_data.py
PYTHONPATH=. streamlit run app/mentor_preview.py
```

## Why this needs ML

- Label = **tomorrow** improves (hidden sleep quality/duration in training only).
- Inputs = **watch signals + lags + vs-your-baseline** — no “how stressed are you?” in the demo.
- Cohort = **Insomnia & Sleep Apnea** only.
- **What-if** tab = actionable “get better” story.

`python scripts/check_session.py`
