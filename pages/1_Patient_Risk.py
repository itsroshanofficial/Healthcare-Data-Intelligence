import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
import streamlit as st

from src import theme
from src.data import AGE_BINS
from src.prediction import predict_patient

st.set_page_config(page_title="Patient Risk Prediction", page_icon="👤", layout="wide")
theme.inject_global_css()
theme.page_header("👤", "Patient Risk Prediction",
                   "Real-time 30-day readmission risk scored by the trained Random Forest model.")

left, right = st.columns([1.1, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Patient Information")

    with st.form("risk_form"):
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("Age Group", AGE_BINS, index=7)
            gender = st.selectbox("Gender", ["Male", "Female"])
            admission_type_id = st.selectbox("Admission Type ID", [1, 2, 3, 5, 6, 7, 8], index=0)
            admission_source_id = st.selectbox("Admission Source ID", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 20, 22], index=6)
            time_in_hospital = st.slider("Time in Hospital (days)", 1, 14, 6)
            num_lab_procedures = st.slider("Number of Lab Procedures", 1, 120, 55)
            num_procedures = st.slider("Number of Procedures", 0, 6, 1)
            num_medications = st.slider("Number of Medications", 1, 80, 31)
        with c2:
            number_outpatient = st.number_input("Outpatient Visits (prior year)", 0, 40, 0)
            number_emergency = st.number_input("Emergency Visits (prior year)", 0, 40, 0)
            number_inpatient = st.number_input("Inpatient Visits (prior year)", 0, 20, 0)
            number_diagnoses = st.slider("Number of Diagnoses", 1, 16, 8)
            insulin = st.selectbox("Insulin", ["No", "Steady", "Up", "Down"])
            change = st.selectbox("Medication Change", ["No", "Ch"], help="'Ch' = medication was changed this visit")
            diabetesMed = st.selectbox("Diabetes Medication Prescribed", ["Yes", "No"])

        submitted = st.form_submit_button("🚨 Predict Readmission Risk")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if submitted:
        patient_data = {
            "age": age, "gender": gender,
            "admission_type_id": admission_type_id, "admission_source_id": admission_source_id,
            "time_in_hospital": time_in_hospital, "num_lab_procedures": num_lab_procedures,
            "num_procedures": num_procedures, "num_medications": num_medications,
            "number_outpatient": number_outpatient, "number_emergency": number_emergency,
            "number_inpatient": number_inpatient, "number_diagnoses": number_diagnoses,
            "insulin": insulin, "change": change, "diabetesMed": diabetesMed,
        }
        result = predict_patient(patient_data)
        prob = result["readmission_probability"]
        level = result["risk_level"]

        gauge_color = {"High": theme.RISK_HIGH, "Medium": theme.RISK_MED, "Low": theme.RISK_LOW}[level]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={"suffix": "%", "font": {"size": 40, "color": theme.NAVY}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": theme.MUTED},
                "bar": {"color": gauge_color, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": theme.RISK_LOW_BG},
                    {"range": [40, 70], "color": theme.RISK_MED_BG},
                    {"range": [70, 100], "color": theme.RISK_HIGH_BG},
                ],
            },
            title={"text": "30-Day Readmission Probability", "font": {"size": 14, "color": theme.MUTED}},
        ))
        fig.update_layout(height=260, margin=dict(t=40, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        messages = {
            "High": "Immediate medical attention and ICU/ER evaluation recommended. Prioritize follow-up scheduling.",
            "Medium": "Patient should be scheduled for a proactive follow-up appointment within the next few days.",
            "Low": "Patient is stable. Standard OPD or general ward monitoring is recommended.",
        }
        theme.result_panel(level, prob, messages[level])
        st.caption("Model: Random Forest · trained on the Diabetes 130-US Hospitals dataset · thresholds: High ≥ 70%, Medium 40–69%, Low < 40%.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 How it works")
        st.write(
            "Fill in the patient's vitals and encounter details, then click "
            "**Predict Readmission Risk**. The form is sent straight into the "
            "project's trained Random Forest pipeline (`models/best_model.pkl`) "
            "— the same model used to score all 20,000+ patients in the "
            "Priority Queue."
        )
        st.markdown(
            f"""
            <div style="margin-top:10px;">
                <span class="badge badge-high">High ≥ 70%</span>&nbsp;
                <span class="badge badge-med">Medium 40–69%</span>&nbsp;
                <span class="badge badge-low">Low &lt; 40%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

theme.footer()
