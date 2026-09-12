# Machine Learning Results

## Dataset

Dataset: Diabetes 130-US Hospitals for Years 1999-2008

The dataset contains hospital encounter records related to diabetes patients.

---

## Prediction Target

The machine learning target was created as:

- `<30` = 1
- `>30` = 0
- `NO` = 0

Target Variable: `readmitted_30`

The objective is to predict whether a patient may be readmitted within 30 days.

---

## Selected Features

The final machine learning features include:

- age
- gender
- admission_type_id
- admission_source_id
- time_in_hospital
- num_lab_procedures
- num_procedures
- num_medications
- number_outpatient
- number_emergency
- number_inpatient
- number_diagnoses
- insulin
- change
- diabetesMed

---

## Data Preprocessing

The following preprocessing steps were performed:

- Missing values were analyzed.
- Missing value indicators such as `?` were identified.
- High-missing-value and irrelevant features were excluded from the final model features.
- Identifier columns were excluded from model features.
- Duplicate records were checked.
- Categorical variables were encoded.
- Numerical and categorical preprocessing was performed using a machine learning pipeline.
- Train and test data were split at the patient level using `patient_nbr` to reduce data leakage.

---

## Train/Test Split

- Training Set: Approximately 80%
- Testing Set: Approximately 20%

Patient-level splitting was used to prevent records from the same patient appearing in both training and testing data.

---

## Models Evaluated

The following machine learning models were evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost

Evaluation metrics included:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

---

## Model Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.672 | 0.157 | 0.476 | 0.237 | 0.627 |
| Random Forest | 0.660 | 0.156 | 0.496 | 0.238 | 0.627 |
| XGBoost | 0.893 | 0.500 | 0.004 | 0.007 | 0.634 |

---

## Selected Model

Random Forest was selected as the final model for this prototype.

Although XGBoost achieved higher overall accuracy, its recall for the positive readmission class was extremely low.

Since the objective is to identify patients who may be readmitted within 30 days, recall for the positive class is important.

Random Forest provided better identification of potential readmission cases and was therefore selected for the patient follow-up priority component.

---

## Patient Follow-up Priority

The predicted readmission probability was converted into follow-up priority categories.

- High Priority: Probability >= 0.70
- Medium Priority: Probability from 0.40 to 0.69
- Low Priority: Probability < 0.40

These thresholds are project-defined decision thresholds and are not clinical guidelines.

---

## Priority Distribution

The generated patient priority results were:

- Medium Priority: 16,024 patients
- Low Priority: 4,003 patients
- High Priority: 126 patients

---

## Limitations

- The dataset is imbalanced because relatively fewer patients were readmitted within 30 days.
- The dataset represents historical hospital encounter data.
- The model should not be used as a clinical diagnosis or treatment system.
- Priority thresholds are project-defined and require clinical validation for real-world healthcare deployment.
- Model performance may change when applied to different hospitals or patient populations.

---

## Conclusion

The machine learning component predicts the probability of 30-day hospital readmission.

This probability is converted into follow-up priority categories and can support the resource optimization component of the system.

The system is designed as a decision-support prototype and does not replace doctors or healthcare professionals.
