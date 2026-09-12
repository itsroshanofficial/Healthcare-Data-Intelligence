# 🏥 AI-Powered Hospital Resource & Patient Priority Intelligence System

A polished, data-driven Streamlit decision-support prototype for patient
readmission risk, follow-up priority, hospital demand and resource planning —
built on the **Diabetes 130-US Hospitals** dataset and a trained Random
Forest model.

## ✨ What's inside

- **Home dashboard** — live KPIs, gradient hero banner with a custom hospital
  illustration, and one-click navigation into every module.
- **Patient Risk Prediction** — a real-time form wired directly to the
  trained model (`models/best_model.pkl`), with a gauge chart and
  color-coded risk panel.
- **Patient Priority Queue** — searchable/filterable triage queue over all
  20,153 real scored patients, with CSV export.
- **Demand Prediction** — 14-day patient volume / bed / ICU demand forecast.
- **Resource Allocation** — gauge-based bed/ICU/staff allocation planner.
- **Advanced Analytics** — model leaderboard (Logistic Regression vs Random
  Forest vs XGBoost), live feature-importance extraction, a correlation
  heatmap, risk-distribution histograms and age-vs-risk trends — all computed
  from the real results CSVs.

A shared design system (`src/theme.py`) keeps colors, cards, badges and the
hero illustration consistent across every page.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```
app.py                     # Home dashboard
pages/
  1_Patient_Risk.py         # Live model inference
  2_Patient_Priority.py     # Real patient triage queue
  3_Demand_Prediction.py    # Forecast charts
  4_Resource_Allocation.py  # Allocation planner
  5_Analytics.py            # Model + data analytics
src/
  theme.py                  # Shared CSS, colors, hero SVG, UI components
  data.py                   # Cached loaders over results/*.csv
  prediction.py             # Model loading + inference + feature importance
  preprocessing.py          # Shared preprocessing hook
models/best_model.pkl       # Trained Random Forest pipeline
results/*.csv                # Real scored patient data (20,153 encounters)
documentation/ML_RESULTS.md  # Full model evaluation write-up
```

## Model summary

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.672 | 0.157 | 0.476 | 0.237 | 0.627 |
| **Random Forest (selected)** | 0.660 | 0.156 | 0.496 | 0.238 | 0.627 |
| XGBoost | 0.893 | 0.500 | 0.004 | 0.007 | 0.634 |

Random Forest was chosen over the higher-accuracy XGBoost because it
actually recalls at-risk patients — critical for a follow-up priority tool.
See `documentation/ML_RESULTS.md` for full methodology and limitations.

## Deployment

Push this repository to GitHub, then deploy `app.py` using Streamlit
Community Cloud (or any platform that supports multipage Streamlit apps).

## Important

This repository contains **de-identified sample/demo-scale data only**. Do
not upload identifiable patient data, credentials, API keys, or private
medical records to GitHub. This is a decision-support prototype and is **not**
a certified medical device — predictions must be validated by qualified
clinicians before any real-world use.
