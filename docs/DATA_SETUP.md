# Dataset setup

## PMData (recommended primary)

**What it is:** Longitudinal Apple Watch data — sleep summaries, heart rate, workouts, etc., from a published study.

**Why we use it:** Matches the product story (consumer wearable, sleep → fatigue).

**Steps**

1. Find the official PMData publication page (search “PMData dataset Apple Watch” — use the authors’ host, often a university archive).
2. Complete their registration / agreement.
3. Download and extract into:

   ```
   data/pmdata/
   ```

4. In Colab, either upload a zip to Drive or rsync from your laptop — **do not commit raw files to GitHub**.

**License:** Follow PMData terms; cite the paper in your presentation.

---

## WESAD (optional / stress extension)

**What it is:** Lab study with chest and wrist sensors; stress/non-stress labels during protocols.

**Why we use it:** Strong **stress** ground truth; good for Week 9+ comparisons.

**Steps**

1. Request access via the UCI / WESAD project page.
2. Extract to `data/wesad/`.
3. Use `notebooks/optional_wesad_stress.ipynb` only after PMData pipeline works.

---

## Demo fallback (no download)

If access is delayed, generate synthetic rows:

```bash
python scripts/generate_demo_data.py
```

This creates `data/sample_demo.csv` (small, committable) with columns aligned to `src/features.py`.

---

## Google Drive layout (team)

```
GDSC-Wearable-ML/
  data/pmdata/          # raw, shared read-only for team
  processed/            # features exports
  models/               # joblib backups
  notebooks/archive/    # weekly Colab exports (.ipynb)
```

Mount in Colab:

```python
from google.colab import drive
drive.mount("/content/drive")
DATA = "/content/drive/MyDrive/GDSC-Wearable-ML/data/pmdata"
```

---

## Citation slide (copy to Google Slides)

- PMData: cite the original paper from the dataset page.
- WESAD: Schmidt et al., WESAD dataset for wearable stress analysis.
- scikit-learn: Pedregosa et al., JMLR 2011.
