# Wearable Stress & Fatigue Prediction — GDSC build track

An **8-session** (or **7-session**) club project for a small team (~5). Use public wearable research data (heart rate, sleep, activity) to predict **fatigue level**, then present a **Streamlit demo** at your GDSC showcase.

All workshops use **Google Colab** + this repo. **No separate homework** — each meeting advances the same codebase.

## Quick start (Session 1)

1. Clone this repo (or open from GitHub in Colab).
2. Read [docs/CURRICULUM.md](docs/CURRICULUM.md).
3. [docs/DATA_SETUP.md](docs/DATA_SETUP.md) — PMData on team Drive (optional WESAD later).
4. Open **`notebooks/week01_kickoff.ipynb`** in [Colab](https://colab.research.google.com/).

## Repository layout

| Path | Purpose |
|------|---------|
| [docs/](docs/) | Curriculum, Colab workflow, mentor guide, presentation checklist |
| [weeks/](weeks/) | Per-session README — what to build **in the room** |
| [notebooks/](notebooks/) | One Colab notebook per session (8 total) |
| [src/](src/) | Shared Python you extend each session |
| [app/](app/) | Streamlit demo (Sessions 7–8) |
| [data/](data/) | Local datasets (see `.gitignore`) |

## Session map

| Session | ML / data focus | Project milestone (in repo) |
|---------|-----------------|-----------------------------|
| 1 | Labels, Colab, Drive | Team charter + first plots |
| 2 | EDA | Figures + data dictionary notes |
| 3 | Feature engineering | `features_v1` + `src/features.py` |
| 4 | Splits & metrics | Baseline + chosen metric |
| 5 | Logistic vs Random Forest | Model comparison |
| 6 | CV, tuning, imbalance | Tuned pipeline |
| 7 | `joblib` + Streamlit | Runnable demo app |
| 8 | Ethics & storytelling | Slides + rehearsal |

Full mentor notes: **[docs/CURRICULUM.md](docs/CURRICULUM.md)** · **[docs/INSTRUCTOR_GUIDE.md](docs/INSTRUCTOR_GUIDE.md)**

## Run the demo (Session 7+)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Datasets

- **PMData** — sleep / HR / activity (primary).
- **WESAD** — optional stress extension (`notebooks/optional_wesad_stress.ipynb`).

We do not redistribute raw data; follow each dataset’s license.

## Team workflow

Branches like `feature/session3-features`, small PRs each session — [team/ROLES.md](team/ROLES.md).

## GitHub

**https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml**

Clone: [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)

## License

MIT — [LICENSE](LICENSE). Respect dataset licenses separately.
