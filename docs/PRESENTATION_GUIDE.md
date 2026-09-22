# GDSC showcase guide (Session 8)

## Format

- ~**10 minutes** + live Streamlit + short Q&A
- Five members: split slides; one person drives the demo

## Google Slides outline

1. Problem — fatigue signals in wearables
2. Data — PMData (+ WESAD if used)
3. Label — rule from team charter
4. Features — top columns table
5. Models — baseline → logistic/RF → tuned
6. Metrics — confusion matrix + why recall or F1
7. Demo — Streamlit screenshot + live run
8. Limitations — not medical advice; lab vs daily life
9. Next steps — personalization, more participants

## Demo script

```bash
streamlit run app/streamlit_app.py
```

Walk through sliders → probability → plain-language message.

## Ethics (read aloud)

“This is a club learning project, not a medical device.”
