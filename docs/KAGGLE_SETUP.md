# Kaggle dataset setup

We use the public **[Sleep Health and Lifestyle Dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)** on Kaggle (sleep duration, quality, stress, heart rate, steps — fits our fatigue/stress story).

## Download (each student or one team copy on Drive)

1. Create a free [Kaggle](https://www.kaggle.com/) account.
2. Open the dataset page → **Download** (or use Kaggle API below).
3. Unzip and place the CSV here:

   ```
   data/kaggle/Sleep_health_and_lifestyle_dataset.csv
   ```

   Exact filename matters — see `src/kaggle_schema.py`.

## Google Colab + Kaggle API (recommended)

1. Kaggle → Account → **Create New API Token** → downloads `kaggle.json`.
2. In Colab:

```python
from google.colab import drive
drive.mount("/content/drive")
# Upload kaggle.json to Drive, then:
!mkdir -p ~/.kaggle
!cp "/content/drive/MyDrive/kaggle.json" ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!pip install -q kaggle
!kaggle datasets download -d uom190346a/sleep-health-and-lifestyle-dataset -p /content/data/kaggle --unzip
```

3. Copy into your cloned repo:

```python
!mkdir -p /content/gdsc-wearable-fatigue-ml/data/kaggle
!cp /content/data/kaggle/Sleep_health_and_lifestyle_dataset.csv /content/gdsc-wearable-fatigue-ml/data/kaggle/
```

## Before Kaggle is ready

```bash
python scripts/generate_demo_data.py
```

Uses `data/sample_demo.csv` — same column names you will build from Kaggle in Session 3.

## Citation (Slides)

Dataset: *Sleep Health and Lifestyle Dataset*, Kaggle (uom190346a). Educational use only; not medical advice.

## Do not commit raw Kaggle CSV to GitHub

`data/kaggle/` is gitignored. Share via team Drive only.
