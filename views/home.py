import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from src import theme
from src.data import priority_counts, load_priority_results, SELECTED_MODEL, MODEL_LEADERBOARD

theme.inject_global_css()

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
theme.hero_banner(
    title_html="AI-Powered Hospital Resource &amp; Patient Priority Intelligence System",
    subtitle=(
        "A decision-support cockpit for patient risk, follow-up priority, "
        "demand forecasting and resource planning — trained on 20,000+ real "
        "hospital encounters."
    ),
)

# ---------------------------------------------------------------------------
# LIVE KPI ROW (real numbers from results/patient_priority_results.csv)
# ---------------------------------------------------------------------------
counts = priority_counts()
df = load_priority_results()
avg_prob = df["Readmission_Probability"].mean() * 100
model_row = MODEL_LEADERBOARD[MODEL_LEADERBOARD["Model"] == SELECTED_MODEL].iloc[0]

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    theme.kpi_card("Patients Analyzed", f"{counts['Total']:,}")
with k2:
    theme.kpi_card("High Priority", f"{counts['High']:,}", "🚨 Immediate follow-up", theme.RISK_HIGH)
with k3:
    theme.kpi_card("Medium Priority", f"{counts['Medium']:,}", "⚠️ Under observation", theme.RISK_MED)
with k4:
    theme.kpi_card("Low Priority", f"{counts['Low']:,}", "✅ Stable", theme.RISK_LOW)
with k5:
    theme.kpi_card("Avg. Readmission Risk", f"{avg_prob:.1f}%", f"Model: {SELECTED_MODEL} · ROC-AUC {model_row['ROC-AUC']:.3f}")

st.write("")
st.markdown("### 🧭 Explore the System")
st.caption("Jump into any module below — every page is powered by the same trained model and real hospital data.")

# ---------------------------------------------------------------------------
# FEATURE NAVIGATION CARDS
# ---------------------------------------------------------------------------
features = [
    {
        "icon": "👤",
        "title": "Patient Risk Prediction",
        "desc": "Score an individual patient's 30-day readmission risk with the trained Random Forest model.",
        "page": "pages/1_Patient_Risk.py",
        "label": "Open Risk Prediction",
    },
    {
        "icon": "🚨",
        "title": "Patient Priority Queue",
        "desc": "Live triage queue of 20k+ real patients, ranked and filterable by follow-up priority.",
        "page": "pages/2_Patient_Priority.py",
        "label": "Open Priority Queue",
    },
    {
        "icon": "📈",
        "title": "Demand Prediction",
        "desc": "Forecast incoming patient volume, bed demand and ICU demand for the next two weeks.",
        "page": "pages/3_Demand_Prediction.py",
        "label": "Open Demand Forecast",
    },
    {
        "icon": "🛏️",
        "title": "Resource Allocation",
        "desc": "Recommended allocation of beds, ICU capacity, doctors and nurses based on current load.",
        "page": "pages/4_Resource_Allocation.py",
        "label": "Open Resource Planner",
    },
    {
        "icon": "📊",
        "title": "Advanced Analytics",
        "desc": "Model leaderboard, feature importance, correlation heatmap and risk distributions.",
        "page": "pages/5_Analytics.py",
        "label": "Open Analytics",
    },
    {
        "icon": "⚙️",
        "title": "Settings",
        "desc": "App info, dataset details, cache controls and important usage disclaimers.",
        "page": "pages/6_Settings.py",
        "label": "Open Settings",
    },
]

cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{feat['icon']}</div>
                <div class="feature-title">{feat['title']}</div>
                <div class="feature-desc">{feat['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(feat["label"], key=f"nav_{i}"):
            st.switch_page(feat["page"])
        st.write("")

theme.footer()
