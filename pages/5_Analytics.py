import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import theme
from src.data import load_priority_results, MODEL_LEADERBOARD, SELECTED_MODEL
from src.prediction import get_feature_importance

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
theme.inject_global_css()
theme.page_header("📊", "Advanced Analytics",
                   "Model performance, feature importance and risk patterns across 20,000+ patients.")

df = load_priority_results()

# ---------------------------------------------------------------------------
# Row 1: Model leaderboard
# ---------------------------------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"##### 🏆 Model Leaderboard — **{SELECTED_MODEL}** selected for production")
lb = MODEL_LEADERBOARD.melt(id_vars="Model", var_name="Metric", value_name="Score")
fig_lb = px.bar(lb, x="Metric", y="Score", color="Model", barmode="group",
                 color_discrete_sequence=[theme.NAVY, theme.TEAL, theme.BLUE])
fig_lb.update_layout(height=340, margin=dict(t=10, b=10, l=10, r=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      legend=dict(orientation="h", y=1.15))
st.plotly_chart(fig_lb, use_container_width=True)
st.caption("XGBoost has the highest raw accuracy, but near-zero recall on the positive (readmitted) class — "
           "it barely flags any at-risk patients. Random Forest was chosen because it actually catches "
           "readmission risk (Recall 0.496), which matters more for a follow-up priority system.")
st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

# ---------------------------------------------------------------------------
# Row 2a: Feature importance
# ---------------------------------------------------------------------------
with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 🔑 What Drives Readmission Risk")
    try:
        fi = get_feature_importance(10)
        fig_fi = px.bar(fi.sort_values("importance"), x="importance", y="feature", orientation="h",
                         color="importance", color_continuous_scale=[theme.TEAL_SOFT, theme.NAVY])
        fig_fi.update_layout(height=360, margin=dict(t=10, b=10, l=10, r=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              coloraxis_showscale=False, yaxis_title="", xaxis_title="Importance")
        st.plotly_chart(fig_fi, use_container_width=True)
        st.caption("Extracted live from the trained Random Forest pipeline (`best_model.pkl`).")
    except Exception as e:
        st.warning(f"Feature importance unavailable: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Row 2b: Risk distribution
# ---------------------------------------------------------------------------
with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 📉 Readmission Probability Distribution")
    fig_hist = px.histogram(df, x="Readmission_Probability", color="Followup_Priority", nbins=40,
                             color_discrete_map={"High": theme.RISK_HIGH, "Medium": theme.RISK_MED, "Low": theme.RISK_LOW})
    fig_hist.update_layout(height=360, margin=dict(t=10, b=10, l=10, r=10),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            legend=dict(orientation="h", y=1.12), xaxis_title="Predicted Probability", yaxis_title="Patients")
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Row 3: Correlation heatmap + Age vs risk
# ---------------------------------------------------------------------------
c3, c4 = st.columns([1.2, 1])
with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 🔗 Feature Correlation Heatmap")
    numeric_cols = ["time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications",
                     "number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses",
                     "Readmission_Probability"]
    corr = df[numeric_cols].corr().round(2)
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale=[theme.TEAL_SOFT, theme.TEAL, theme.NAVY],
                          aspect="auto")
    fig_corr.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 👥 Avg. Risk by Age Group")
    age_risk = df.groupby("age")["Readmission_Probability"].mean().reset_index()
    age_risk["age_order"] = age_risk["age"].str.extract(r"\[(\d+)").astype(int)
    age_risk = age_risk.sort_values("age_order")
    fig_age = px.bar(age_risk, x="age", y="Readmission_Probability", color="Readmission_Probability",
                      color_continuous_scale=[theme.RISK_LOW, theme.RISK_MED, theme.RISK_HIGH])
    fig_age.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, xaxis_title="Age Group", yaxis_title="Avg. Predicted Risk")
    st.plotly_chart(fig_age, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("All charts on this page are computed live from `results/patient_priority_results.csv` "
           "(20,153 real patient encounters) and the trained model leaderboard in `documentation/ML_RESULTS.md`.")
theme.footer()
