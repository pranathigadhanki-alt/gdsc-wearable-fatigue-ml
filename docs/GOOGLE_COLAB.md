# Google Colab workflow

## Open notebooks

Upload from `notebooks/` or clone the repo in the first cell of each session notebook.

## Standard setup cell

```python
!git clone https://github.com/pranathigadhanki-alt/gdsc-wearable-fatigue-ml.git
%cd gdsc-wearable-fatigue-ml
!pip install -q -r requirements.txt
```

## Google Drive (team data)

```python
from google.colab import drive
drive.mount("/content/drive")
DATA = "/content/drive/MyDrive/GDSC-Wearable-ML/data/pmdata"
```

## Google tools by session

| Session | Tool |
|---------|------|
| 1 | Drive mount, shared folder |
| 2 | Sheets optional (data dictionary) |
| 6 | Colab + imbalanced-learn |
| 8 | **Google Slides** for showcase |

## Saving work

Commit notebook changes to GitHub via PR — that is the project record. Optionally copy `.ipynb` to Drive for backup.

## Secrets

Do not commit credentials or raw PMData to GitHub.
