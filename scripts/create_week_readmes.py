#!/usr/bin/env python3
"""Create weeks/weekNN/README.md for 8 GDSC sessions."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

SESSIONS = [
    (1, "Kickoff", "Supervised labels, Colab, Drive", "week01_kickoff.ipynb", "Team charter merged; notebook runs; label plot"),
    (2, "EDA", "Distributions & correlation", "week02_eda.ipynb", "Notebook holds 3 plots + insight bullets"),
    (3, "Features", "Sleep/HR feature table", "week03_features.ipynb", "`src/features.py` updated; features path on Drive"),
    (4, "Splits & metrics", "Group splits, baselines, F1/recall", "week04_splits_and_metrics.ipynb", "Metric chosen; baseline + confusion matrix"),
    (5, "Model compare", "Logistic vs Random Forest", "week05_model_compare.ipynb", "Comparison table; pick model family"),
    (6, "Tuning & imbalance", "CV, GridSearch, class weights", "week06_tuning_and_imbalance.ipynb", "Tuned pipeline + best_params.json"),
    (7, "Streamlit", "joblib + demo app", "week07_model_and_streamlit.ipynb", "Everyone runs Streamlit once; PR merged"),
    (8, "Showcase", "Ethics, Slides, rehearsal", "week08_showcase.ipynb", "Slides linked; dry-run demo"),
]

TEMPLATE = """# Session {n}: {title}

**ML focus:** {ml}

**Notebook:** [`notebooks/{notebook}`](../../notebooks/{notebook}) · [Colab workflow](../../docs/GOOGLE_COLAB.md)

## Goal for this meeting

Advance the **shared project** — not a separate assignment. By adjournment:

**{output}**

## Suggested flow (~90–120 min)

1. Quick concept (mentor) — see [docs/INSTRUCTOR_GUIDE.md](../../docs/INSTRUCTOR_GUIDE.md)
2. Run notebook together in Colab
3. Pairs edit `src/` or `app/`; open a PR before you leave
4. If time runs out, start next session by finishing the same PR

## Checklist

- [ ] `git pull origin main` at start
- [ ] Notebook runs top-to-bottom
- [ ] At least one PR merged or ready for review
"""


def main() -> None:
    weeks_dir = ROOT / "weeks"
    for child in weeks_dir.iterdir():
        if child.is_dir() and child.name.startswith("week"):
            num = child.name.replace("week", "")
            if num.isdigit() and int(num) > 8:
                shutil.rmtree(child)
                print("Removed", child)

    for n, title, ml, notebook, output in SESSIONS:
        folder = weeks_dir / f"week{n:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(
            TEMPLATE.format(n=n, title=title, ml=ml, notebook=notebook, output=output)
        )
    print("Session READMEs written (8 weeks).")


if __name__ == "__main__":
    main()
