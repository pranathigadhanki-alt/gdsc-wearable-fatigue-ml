# GDSC mentor guide

This track is for a **Google Developer Student Clubs** build sprint: one shared repo, one Streamlit demo, ~5 members, **7–8 weekly workshops**. No assignments outside the room — progress *is* the project.

## Before the first session

1. Request **PMData** access early; put raw files in a **read-only Drive folder** (never commit raw data).
2. Create GitHub repo; add members as collaborators.
3. Share Drive + Colab link + [team/ROLES.md](../team/ROLES.md).
4. Skim [docs/CURRICULUM.md](CURRICULUM.md) and pick **7 or 8** sessions on your club calendar.

## Session template (~90–120 min)

| Block | Time | Activity |
|-------|------|----------|
| Concept | 15 min | One ML idea on the whiteboard |
| Demo | 20 min | Mentor runs Colab; members follow |
| Build | 45 min | Pairs work on **repo tasks** (features, models, app) |
| Integrate | 15 min | One merged PR to `main` before adjourn |
| Next | 5 min | Name the first task if you ran long (still in-project, not homework) |

## What “done” looks like (club outcome)

- Mentees complete **[BUILD_PATH.md](BUILD_PATH.md)** — `python scripts/check_session.py` shows “Dashboard ready”
- **`streamlit run app/streamlit_app.py`** matches **`mentor_preview`** (same `app/dashboard.py`)
- Slides cite Kaggle Sleep Health dataset + non-medical disclaimer

## Common pitfalls

- **Leakage:** Same-night features predicting same-night label — use participant-day groups (Session 4).
- **Scope creep:** Skip deep learning; sklearn pipeline is enough for the showcase.
- **Colab drift:** Always `git pull` at start of session; one branch per pair.

## If PMData is late

Use `data/sample_demo.csv` for Sessions 1–6; swap paths when real data lands — the pipeline stays the same.

## 7-session calendar

| Week | Sessions covered |
|------|------------------|
| 1 | 1 + light EDA |
| 2 | 3 Features |
| 3 | 4 Metrics/splits |
| 4 | 5 Models |
| 5 | 6 Tuning |
| 6 | 7 Streamlit |
| 7 | 8 Showcase |

Skip standalone Session 2 EDA depth until PMData exists, or run a 30-minute EDA block in Session 1.
