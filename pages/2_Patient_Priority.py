import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.express as px
import streamlit as st

from src import theme
from src.data import load_priority_results, priority_counts

st.set_page_config(page_title="Patient Priority Queue", page_icon="🚨", layout="wide")
theme.inject_global_css()
theme.page_header("🚨", "Patient Priority Queue",
                   "Real-time triage queue across 20,000+ scored patient encounters.")

counts = priority_counts()
c1, c2, c3 = st.columns(3)
with c1:
    theme.kpi_card("🚨 High Priority", f"{counts['High']:,}", "Needs immediate follow-up", theme.RISK_HIGH)
with c2:
    theme.kpi_card("⚠️ Medium Priority", f"{counts['Medium']:,}", "Under observation", theme.RISK_MED)
with c3:
    theme.kpi_card("✅ Low Priority", f"{counts['Low']:,}", "Stable / outpatient", theme.RISK_LOW)

st.write("")

df = load_priority_results()

col_chart, col_filters = st.columns([1, 1.6])
with col_chart:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### Priority Mix")
    pie = px.pie(
        df, names="Followup_Priority", hole=0.55,
        color="Followup_Priority",
        color_discrete_map={"High": theme.RISK_HIGH, "Medium": theme.RISK_MED, "Low": theme.RISK_LOW},
    )
    pie.update_traces(textinfo="percent+label")
    pie.update_layout(height=260, margin=dict(t=10, b=10, l=10, r=10), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_filters:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### Search &amp; Filter")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        search = st.text_input("🔍 Patient ID", "")
    with fc2:
        priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    with fc3:
        age_filter = st.selectbox("Age Group", ["All"] + sorted(df["age"].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

filtered = df.copy()
if priority_filter != "All":
    filtered = filtered[filtered["Followup_Priority"] == priority_filter]
if age_filter != "All":
    filtered = filtered[filtered["age"] == age_filter]
if search:
    filtered = filtered[filtered["Patient_ID"].str.contains(search, case=False)]

filtered = filtered.sort_values("Readmission_Probability", ascending=False)

st.markdown("#### 📋 Active Priority Queue")
st.caption(f"Showing {len(filtered):,} of {len(df):,} patients, ranked by readmission probability.")

display_cols = ["Patient_ID", "age", "gender", "time_in_hospital", "num_medications",
                 "number_inpatient", "Readmission_Probability", "Followup_Priority"]
show_df = filtered[display_cols].head(500).rename(columns={
    "Patient_ID": "Patient ID", "age": "Age", "gender": "Gender",
    "time_in_hospital": "Days in Hospital", "num_medications": "Medications",
    "number_inpatient": "Prior Inpatient Visits",
    "Readmission_Probability": "Readmission Risk", "Followup_Priority": "Priority",
})
show_df["Readmission Risk"] = (show_df["Readmission Risk"] * 100).round(1).astype(str) + "%"

st.dataframe(show_df, use_container_width=True, hide_index=True, height=420)
if len(filtered) > 500:
    st.caption("Displaying the top 500 matching patients by risk for readability. Use filters to narrow further.")

st.download_button(
    "⬇️ Download filtered queue as CSV",
    data=filtered[display_cols].to_csv(index=False).encode("utf-8"),
    file_name="filtered_priority_queue.csv",
    mime="text/csv",
)

theme.footer()
