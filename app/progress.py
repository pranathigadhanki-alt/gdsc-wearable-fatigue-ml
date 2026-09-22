"""Session checks for StrainScope build path."""

from __future__ import annotations

import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS: list[tuple[int, str, str, str]] = [
    (1, "load_kaggle_raw", "src.data_loader", "load_kaggle_raw"),
    (3, "load_feature_table", "src.data_loader", "load_feature_table"),
    (3, "load_person_baselines", "src.data_loader", "load_person_baselines"),
    (3, "build_features_from_kaggle", "src.features", "build_features_from_kaggle"),
    (3, "strain_label", "src.features", "strain_label"),
    (4, "participant_groups", "src.data_loader", "participant_groups"),
    (4, "evaluate_classifier", "src.metrics_utils", "evaluate_classifier"),
    (5, "build_logistic_pipeline", "src.models", "build_logistic_pipeline"),
    (5, "build_rf_pipeline", "src.models", "build_rf_pipeline"),
    (7, "train_model", "src.models", "train_model"),
    (7, "predict_strain", "src.models", "predict_strain"),
    (7, "explain_prediction", "src.explain", "explain_prediction"),
    (7, "suggest_what_ifs", "src.counterfactuals", "suggest_what_ifs"),
]

DASHBOARD_REQUIRES = {
    "load_feature_table",
    "load_person_baselines",
    "train_model",
    "predict_strain",
    "explain_prediction",
    "suggest_what_ifs",
}


def _run_check(module_name: str, func_name: str) -> tuple[bool, str]:
    try:
        mod = importlib.import_module(module_name)
        fn = getattr(mod, func_name)
        if func_name == "load_kaggle_raw":
            try:
                fn()
            except FileNotFoundError:
                pass
        elif func_name == "load_feature_table":
            df = fn(use_demo=True)
            if "strain_high" not in df.columns:
                return False, "missing strain_high"
        elif func_name == "load_person_baselines":
            fn(use_demo=True)
        elif func_name == "build_features_from_kaggle":
            import pandas as pd

            raw = pd.DataFrame(
                {
                    "Person ID": [1, 1],
                    "Sleep Duration": [7.0, 6.0],
                    "Quality of Sleep": [6, 5],
                    "Physical Activity Level": [40, 35],
                    "Stress Level": [5, 8],
                    "Heart Rate": [70, 76],
                    "Daily Steps": [6000, 4000],
                    "Age": [25, 25],
                    "Gender": ["Male", "Male"],
                }
            )
            out = fn(raw)
            if "sleep_duration_delta" not in out.columns:
                return False, "missing deltas"
        elif func_name == "strain_label":
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            if len(fn(df)) != len(df):
                return False, "bad length"
        elif func_name == "participant_groups":
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            fn(df)
        elif func_name == "evaluate_classifier":
            fn([0, 1, 0], [0, 0, 1])
        elif func_name in ("build_logistic_pipeline", "build_rf_pipeline"):
            fn()
        elif func_name == "train_model":
            fn(use_demo=True)
        elif func_name == "predict_strain":
            from src.models import train_model, FEATURE_COLUMNS
            import pandas as pd

            pipe = train_model(use_demo=True)
            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            row = df[FEATURE_COLUMNS].iloc[0].to_dict()
            fn(row, pipe)
        elif func_name == "explain_prediction":
            from src.models import train_model, FEATURE_COLUMNS
            from src.data_loader import load_person_baselines
            import pandas as pd

            df = pd.read_csv(ROOT / "data" / "sample_demo.csv")
            baselines = load_person_baselines(use_demo=True)
            pipe = train_model(use_demo=True)
            row = df[FEATURE_COLUMNS].iloc[0].to_dict()
            fn(row, baselines, df["participant_id"].iloc[0], pipe, 0, 0.4)
        elif func_name == "suggest_what_ifs":
            from src.models import train_model
            from src.data_loader import load_person_baselines

            baselines = load_person_baselines(use_demo=True)
            pipe = train_model(use_demo=True)
            today = {
                "sleep_duration": 6.5,
                "heart_rate": 75,
                "daily_steps": 5000,
                "physical_activity_level": 40,
            }
            fn(1, today, baselines, pipe, 0.5)
        return True, "OK"
    except NotImplementedError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def session_status() -> list[str]:
    lines: list[str] = []
    current = None
    for sess, _, mod, func in CHECKS:
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
