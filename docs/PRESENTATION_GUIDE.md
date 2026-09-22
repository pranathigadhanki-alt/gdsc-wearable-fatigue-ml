# Showcase — StrainScope (Session 8)

## 10-minute flow

1. **Hook (30s)** — “Your watch already knows something’s off before you admit you’re drained.”
2. **Problem** — Survey fatigue; we use passive signals + **your** baseline.
3. **Live demo** — Pick Person 12 → “Short sleep + high HR” preset → gauge → **What moves the needle?** (+1h sleep).
4. **ML moment** — One slide: rules vs RF on held-out people (precision/recall).
5. **Tech** — sklearn, group splits, Kaggle dataset citation.
6. **Limits** — Not medical; labels from self-report in training; demo CSV ≠ your real watch.

## Demo script

```bash
PYTHONPATH=. streamlit run app/streamlit_app.py
```

1. Sidebar: choose person  
2. Tab 1: bad-day preset → Estimate  
3. Tab 2: read “Compared to you”  
4. Tab 3: read top what-if (green ↓ pp)

## Ethics (read aloud)

“This is a student learning project, not a medical device or diagnosis tool.”
