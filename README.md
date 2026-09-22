# GDSC — Wearable fatigue ML (week-by-week build)

Eight in-room sessions: mentees implement **`src/`** step by step until **`streamlit run app/streamlit_app.py`** matches the **mentor preview** (colorful gauge, presets, “Why this score?” explanations).

**Dataset:** [Kaggle — Sleep Health and Lifestyle](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)

| Role | Start here |
|------|------------|
| **Mentee** | [docs/BUILD_PATH.md](docs/BUILD_PATH.md) → Session 1 notebook |
| **Mentor** | [docs/MENTOR.md](docs/MENTOR.md) · `PYTHONPATH=. streamlit run app/mentor_preview.py` |

**Repo:** https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml

```bash
git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git
cd gdsc-wearable-fatigue-ml
pip install -r requirements.txt
python scripts/generate_demo_data.py
python scripts/check_session.py   # progress toward full app
```

## How the preview fits in

| Session | Mentee work | App state |
|---------|-------------|-----------|
| 1–6 | `src/` + notebooks | Progress screen in `streamlit_app.py` |
| 7 | models + explain | **Full dashboard** (same as mentor preview) |
| 8 | Slides + demo | Same app at showcase |

Shared UI: `app/dashboard.py` · Checks: `app/progress.py` / `scripts/check_session.py`

## Layout

- `src/` — fill-in-the-blank (your code)
- `solutions/` — mentor reference
- `weeks/` + `notebooks/` — one session each
- `app/` — theme + dashboard + streamlit entrypoints

MIT [LICENSE](LICENSE) — cite Kaggle dataset on slides.
