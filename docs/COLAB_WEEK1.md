# Week 1 — Colab (share these links)

## Open Session 1 notebook in Colab

**One-click:**  
https://colab.research.google.com/github/pranathigadhanki-alt/gdsc-wearable-fatigue-ml/blob/main/notebooks/week01_kickoff.ipynb

Mentees: **File → Save a copy in Drive** so edits stay in their Drive.

## Repo on Colab (after clone cell)

| Path | What it is |
|------|------------|
| `/content/gdsc-wearable-fatigue-ml/` | Repo root (same as `%cd` target) |
| `src/data_loader.py` | **Session 1** — implement `load_kaggle_raw` |
| `src/kaggle_schema.py` | Expected Kaggle filename + column names |
| `data/kaggle/Sleep_health_and_lifestyle_dataset.csv` | Team CSV (from Drive — **not** in Git) |
| `data/sample_demo.csv` | Demo nights (run `generate_demo_data.py`) |
| `docs/KAGGLE_SETUP.md` | Download / API instructions |
| `templates/team_charter.md` | Copy → `team/team_charter.md` |
| `app/mentor_preview.py` | Full UI (mentor); mentees use `streamlit_app.py` from Session 7 |

## Team Drive folder (suggested)

`/content/drive/MyDrive/GDSC-RecoveryScope/`

- `kaggle/Sleep_health_and_lifestyle_dataset.csv` — one shared copy  
- Optional: backups of notebooks  

Copy into repo after mount:

```python
from pathlib import Path
import shutil
drive_csv = Path("/content/drive/MyDrive/GDSC-RecoveryScope/kaggle/Sleep_health_and_lifestyle_dataset.csv")
repo_kaggle = Path("/content/gdsc-wearable-fatigue-ml/data/kaggle")
repo_kaggle.mkdir(parents=True, exist_ok=True)
if drive_csv.exists():
    shutil.copy(drive_csv, repo_kaggle / drive_csv.name)
    print("Copied to", repo_kaggle)
else:
    print("Upload CSV to Drive path above, or use docs/KAGGLE_SETUP.md API")
```

## Mentor screen-share order

1. Open Colab link above  
2. Run Drive mount → clone → pip → `generate_demo_data.py`  
3. Show `load_feature_table(use_demo=True).head()`  
4. Show `data/kaggle/` empty until CSV copied  
5. (Optional) local preview: `streamlit run app/mentor_preview.py` on your laptop  
