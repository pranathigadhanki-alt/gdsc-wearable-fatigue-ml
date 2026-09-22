# 8-session GDSC curriculum

**One club meeting = one step forward on the same project.** There is no separate homework — whatever you do not finish in the room becomes the opening task next session (or a paired task during the meeting).

**Stack every session:** [Google Colab](https://colab.research.google.com/) + shared [Google Drive](https://drive.google.com/) + this GitHub repo.

**Team size:** ~5 members — see [team/ROLES.md](../team/ROLES.md).

---

## Session 1 — Kickoff: problem, data, Colab

**ML topic:** Supervised classification; choosing a label (fatigue proxy from sleep + HR).

**Google tools:** Colab, Drive mount, shared team folder.

**In-room project work**

1. Agree on user story and fill [templates/team_charter.md](../templates/team_charter.md) in the repo (PR before you leave).
2. Clone repo in Colab; run demo data; plot label balance.
3. Start PMData access (mentor may have already downloaded to Drive).

**Session output:** Charter merged + `notebooks/week01_kickoff.ipynb` runs end-to-end.

→ [weeks/week01/README.md](../weeks/week01/README.md)

---

## Session 2 — EDA on real or demo data

**ML topic:** Distributions, missing values, correlation — what might predict fatigue?

**Google tools:** Colab plots; optional **Google Sheets** for a shared “data dictionary”.

**In-room project work:** 3 figures and short bullet notes **in the notebook**; decide which columns map from PMData.

**Session output:** Updated notebook + notes that drive Session 3 features.

---

## Session 3 — Feature table

**ML topic:** Domain features (sleep efficiency, stage ratios, resting HR, steps).

**Google tools:** Colab; export `features_v1.csv` to team Drive (not raw PMData in git).

**In-room project work:** Extend `src/features.py`; build nightly rows; apply rule-based `fatigue_high` from charter.

**Session output:** Processed feature path documented in `src/data_loader.py` / team Drive.

---

## Session 4 — Splits, leakage, metrics

**ML topics:** Group split by participant-day; dummy baseline; precision/recall/F1/confusion matrix.

**Google tools:** Colab `sklearn.metrics`.

**In-room project work:** Train/test split without leakage; baseline score; **team picks one primary metric** (usually recall on high fatigue) and records it in the charter.

**Session output:** Metric table + confusion matrix in `notebooks/week04_splits_and_metrics.ipynb`.

---

## Session 5 — Logistic regression vs Random Forest

**ML topics:** Scaling + logistic regression; tree ensembles; feature importance.

**Google tools:** Colab.

**In-room project work:** Two pipelines in `src/models.py`; compare on validation split from Session 4.

**Session output:** Leaderboard cell in notebook; best-so-far model identified.

---

## Session 6 — Tuning & class imbalance

**ML topics:** Cross-validation, `GridSearchCV`, `class_weight` / optional SMOTE.

**Google tools:** Colab + imbalanced-learn.

**In-room project work:** Tune the stronger family from Session 5; document tradeoff (recall vs precision) in notebook markdown.

**Session output:** `models/best_params.json` (params only) + tuned pipeline.

---

## Session 7 — Lock model + Streamlit

**ML topics:** Model selection, `joblib`, inference inputs.

**Google tools:** Colab for training; local or Codespaces for Streamlit if needed.

**In-room project work:** Save final model; wire `app/streamlit_app.py` to real feature columns; everyone runs the app once.

**Session output:** Merged PR with model artifact on Drive + working Streamlit.

---

## Session 8 — Showcase rehearsal

**ML topic:** Responsible ML — limitations, not medical advice, dataset bias.

**Google tools:** **Google Slides** ([PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)).

**In-room project work:** Polish slides, demo script, app copy; dry-run 10-minute presentation.

**Session output:** Slide link in repo README + recorded or live demo ready for GDSC event.

---

## Only 7 sessions?

Merge **Session 2 into 1** (shorter EDA on demo data only), or merge **Session 8 into 7** (slides + Streamlit same day). Keep the same project milestones; skip optional WESAD.

## Optional extension

`notebooks/optional_wesad_stress.ipynb` — after PMData pipeline works, for members who want extra challenge.
