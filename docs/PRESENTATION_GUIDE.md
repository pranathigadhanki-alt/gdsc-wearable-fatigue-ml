# Showcase — RecoveryScope (Session 8)

## 10-minute flow

1. **Hook (30s)** — “If you have insomnia or sleep apnea, will *tomorrow* be a better night? Your watch + last night hint at the answer.”
2. **Problem** — One-row surveys miss **night-to-night** recovery; we use watch signals, **your baseline**, and **lags**.
3. **Live demo** — Pick someone with Insomnia → set last night + tonight → gauge **chance of better night tomorrow** → **Get better tomorrow** tab (what-if).
4. **ML moment** — Rules vs RF on held-out people; label uses next-night quality/duration (training only).
5. **Tech** — sklearn, group splits, Kaggle Sleep Health & Lifestyle (disorder cohort).
6. **Limits** — Not a sleep study; not diagnosis or treatment advice; demo data is synthetic nights.

## Demo script

```bash
python scripts/generate_demo_data.py
PYTHONPATH=. streamlit run app/mentor_preview.py
```

1. Sidebar: person + disorder label  
2. Tab **Tonight**: last night + tonight sliders → Estimate  
3. Tab **Why**: plain-language drivers vs your baseline  
4. Tab **Get better tomorrow**: top changes that **raise** recovery probability  

## Ethics (read aloud)

“This is a GDSC learning project on public data. It does **not** replace a sleep study, CPAP, or care from a doctor.”
