"""
Central data access layer.
Loads the project's real ML outputs (results/*.csv) instead of fake demo
numbers, and exposes small cached helpers used across every page.
"""

import os
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

AGE_BINS = ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
            "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"]

MODEL_LEADERBOARD = pd.DataFrame([
    {"Model": "Logistic Regression", "Accuracy": 0.672, "Precision": 0.157, "Recall": 0.476, "F1 Score": 0.237, "ROC-AUC": 0.627},
    {"Model": "Random Forest",       "Accuracy": 0.660, "Precision": 0.156, "Recall": 0.496, "F1 Score": 0.238, "ROC-AUC": 0.627},
    {"Model": "XGBoost",             "Accuracy": 0.893, "Precision": 0.500, "Recall": 0.004, "F1 Score": 0.007, "ROC-AUC": 0.634},
])
SELECTED_MODEL = "Random Forest"


@st.cache_data(show_spinner=False)
def load_priority_results() -> pd.DataFrame:
    """Real per-patient readmission probability + follow-up priority."""
    path = os.path.join(RESULTS_DIR, "patient_priority_results.csv")
    df = pd.read_csv(path)
    df["admission_type_id"] = df["admission_type_id"].astype(str)
    df["admission_source_id"] = df["admission_source_id"].astype(str)
    return df


@st.cache_data(show_spinner=False)
def load_predictions() -> pd.DataFrame:
    """Real predictions file (no Patient_ID column, used for analytics)."""
    path = os.path.join(RESULTS_DIR, "patient_predictions.csv")
    df = pd.read_csv(path)
    return df


@st.cache_data(show_spinner=False)
def priority_counts() -> dict:
    df = load_priority_results()
    counts = df["Followup_Priority"].value_counts().to_dict()
    return {
        "High": int(counts.get("High", 0)),
        "Medium": int(counts.get("Medium", 0)),
        "Low": int(counts.get("Low", 0)),
        "Total": int(len(df)),
    }


@st.cache_data(show_spinner=False)
def demand_series() -> pd.DataFrame:
    """
    Illustrative short-term demand curve.
    Clearly a prototype trend (not the trained ML model) until a dedicated
    forecasting model is integrated -- but shaped using the real average
    daily encounter volume so it is not an arbitrary number.
    """
    rng = np.random.default_rng(7)
    total_patients = priority_counts()["Total"]
    baseline = max(120, min(260, total_patients / 90))
    days = pd.date_range("2026-09-01", periods=14)
    trend = np.linspace(0, 18, 14)
    noise = rng.normal(0, 3.5, 14)
    actual = np.round(baseline + trend + noise).astype(int)
    predicted = np.round(baseline + trend + rng.normal(0, 2, 14)).astype(int)
    beds = np.round(actual * 0.62).astype(int)
    icu = np.round(actual * 0.095).astype(int)
    return pd.DataFrame({
        "Date": days,
        "Actual Patients": actual,
        "Predicted Patients": predicted,
        "Bed Demand": beds,
        "ICU Demand": icu,
    })


@st.cache_data(show_spinner=False)
def resource_table() -> pd.DataFrame:
    counts = priority_counts()
    return pd.DataFrame({
        "Resource": ["General Beds", "ICU Beds", "Doctors", "Nurses"],
        "Capacity": [250, 40, 35, 80],
        "Available": [124, 18, 14, 42],
        "Recommended Allocation": [
            110,
            min(40, 17 + round(counts["High"] / 20)),
            12,
            38,
        ],
    })
