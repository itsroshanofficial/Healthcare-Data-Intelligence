import os
import warnings

import joblib
import pandas as pd

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path of saved model
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")

# Exact features used during model training (order matters)
FEATURE_COLUMNS = [
    "age",
    "gender",
    "admission_type_id",
    "admission_source_id",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "insulin",
    "change",
    "diabetesMed",
]

_model = None


def get_model():
    """Lazily load the trained sklearn Pipeline (cached at module level)."""
    global _model
    if _model is None:
        with warnings.catch_warnings():
            # The pickle was trained on a slightly newer scikit-learn; this
            # only affects repr()/get_params(), not predict(), so it's safe
            # to silence for the app's purposes.
            warnings.simplefilter("ignore")
            _model = joblib.load(MODEL_PATH)
    return _model


def predict_patient(patient_data: dict) -> dict:
    """
    Predicts 30-day readmission probability using the trained Random Forest
    pipeline and converts it into a follow-up risk/priority level using the
    same thresholds documented in documentation/ML_RESULTS.md.
    """
    model = get_model()

    patient_df = pd.DataFrame([patient_data])[FEATURE_COLUMNS]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        probability = float(model.predict_proba(patient_df)[0][1])
        prediction = int(model.predict(patient_df)[0])

    if probability >= 0.70:
        risk_level = "High"
    elif probability >= 0.40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "prediction": prediction,
        "readmission_probability": round(probability, 4),
        "risk_level": risk_level,
    }


def get_feature_importance(top_n: int = 12) -> pd.DataFrame:
    """
    Extracts feature importances from the trained Random Forest pipeline,
    mapping the one-hot encoded column names back to human-readable labels.
    """
    model = get_model()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        preprocessor = model.named_steps["preprocessor"]
        classifier = model.named_steps["model"]
        names = preprocessor.get_feature_names_out()
        importances = classifier.feature_importances_

    df = pd.DataFrame({"feature": names, "importance": importances})
    df["feature"] = (
        df["feature"]
        .str.replace(r"^num__", "", regex=True)
        .str.replace(r"^cat__", "", regex=True)
        .str.replace("_", " ")
    )
    df = df.groupby("feature", as_index=False)["importance"].sum()
    df = df.sort_values("importance", ascending=False).head(top_n)
    return df.reset_index(drop=True)
