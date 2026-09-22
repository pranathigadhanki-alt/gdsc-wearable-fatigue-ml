# Session 7: Full preview app

**Notebook:** [`notebooks/week07_model_and_streamlit.ipynb`](../../notebooks/week07_model_and_streamlit.ipynb)  
**Build guide:** [docs/BUILD_PATH.md](../../docs/BUILD_PATH.md) (Session 7)  
**Check progress:** `python scripts/check_session.py`

## Edit this session

**Primary file(s):** `src/models.py, src/explain.py`

## Done when

- [ ] `train_model`, `predict_fatigue`, `explain_prediction`
- [ ] `PYTHONPATH=. streamlit run app/streamlit_app.py` → same UI as mentor preview
- [ ] `python scripts/check_session.py` → Dashboard ready

## Flow (~90–120 min)

1. Mentor concept (5–15 min)
2. Work through the notebook in Colab
3. Implement the `src/` TODOs for this session
4. PR before you leave; run `check_session.py`

## Preview alignment

The final app (`app/streamlit_app.py`) uses `app/dashboard.py` — **you do not rewrite the UI**. Each session adds backend logic until Session 7 unlocks the full colorful dashboard (gauge, explanations, presets).
