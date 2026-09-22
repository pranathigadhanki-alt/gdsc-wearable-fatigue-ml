"""Session completion checks for the mentee Streamlit app."""

from __future__ import annotations

import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS: list[tuple[int, str, str, str]] = [
    (1, "load_kaggle_raw", "src.data_loader", "load_kaggle_raw"),
    (3, "load_feature_table", "src.data_loader", "load_feature_table"),
    (3, "build_features_from_kaggle", "src.features", "build_features_from_kaggle"),
    (3, "fatigue_label", "src.features", "fatigue_label"),
    (4, "participant_groups", "src.data_loader", "participant_groups"),
    (4, "evaluate_classifier", "src.metrics_utils", "evaluate_classifier"),
    (5, "build_logistic_pipeline", "src.models", "build_logistic_pipeline"),
    (5, "build_rf_pipeline", "src.models", "build_rf_pipeline"),
    (7, "train_model", "src.models", "train_model"),
    (7, "predict_fatigue", "src.models", "predict_fatigue"),
    (7, "explain_prediction", "src.explain", "explain_prediction"),
]

DASHBOARD_REQUIRES = {
    "load_feature_table",
    "train_model",
    "predict_fatigue",
    "explain_prediction",
}


def _run_check(module_name: str, func_name: str) -> tuple[bool, str]:
    try:
        mod = importlib.import_module(module_name)
        fn = getattr(mod, func_name)

        if func_name == "load_kaggle_raw":
            path = ROOT / "data" / "kaggle" / "Sleep_health_and_lifestyle_dataset.csv"
            if path.exists():
                fn(path)
            else:
                # Implemented if we get past NotImplementedError
                try:
                    fn()
                except FileNotFoundError:
                    pass
        elif func_name == "load_feature_table":
            df = fn(use_demo=True)
            if "fatigue_high" not in df.columns:
                return False, "missing fatigue_high column"
        elif func_name == "build_features_from_kaggle":
            import pandas as pd

            raw = pd.DataFrame(
                {
                    "Person ID": [1],
                    "Sleep Duration": [7.0],
                    "Quality of Sleep": [6],
                    "Physical Activity Level": [40],
                    "Stress Level": [5],
                    "Heart Rate": [70],
                    "Daily Steps": [6000],
                    "Age": [25],
                    "Gender": ["Male"],
                }
            )
            out = fn(raw)
            if "participant_id" not in out.columns:
                return False, "missing participant_id"
        elif func_name == "fatigue_label":
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            if len(fn(df)) != len(df):
                return False, "wrong length"
        elif func_name == "participant_groups":
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            if len(fn(df)) != len(df):
                return False, "wrong length"
        elif func_name == "evaluate_classifier":
            fn([0, 1, 0], [0, 0, 0])
        elif func_name in ("build_logistic_pipeline", "build_rf_pipeline"):
            fn()
        elif func_name == "train_model":
            fn(use_demo=True)
        elif func_name == "predict_fatigue":
            from src.models import train_model

            pipe = train_model(use_demo=True)
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            from src.models import FEATURE_COLUMNS

            row = {c: float(df[c].iloc[0]) for c in FEATURE_COLUMNS}
            fn(row, pipe)
        elif func_name == "explain_prediction":
            from src.models import FEATURE_COLUMNS, train_model
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            pipe = train_model(use_demo=True)
            row = {c: float(df[c].iloc[0]) for c in FEATURE_COLUMNS}
            fn(row, df, pipe, 0, 0.3)
        return True, "OK"
    except NotImplementedError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def session_status() -> list[str]:
    lines: list[str] = []
    current = None
    for sess, label, mod, func in CHECKS:
        if sess != current:
            current = sess
            lines.append(f"**Session {sess}**")
        ok, msg = _run_check(mod, func)
        icon = "✅" if ok else "⬜"
        lines.append(f"- {icon} `{func}` — {msg}")
    return lines


def ready_for_dashboard() -> bool:
    for _, label, mod, func in CHECKS:
        if label not in DASHBOARD_REQUIRES:
            continue
        ok, _ = _run_check(mod, func)
        if not ok:
            return False
    return True
