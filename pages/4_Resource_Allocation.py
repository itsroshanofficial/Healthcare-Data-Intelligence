import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
import streamlit as st

from src import theme
from src.data import resource_table

st.set_page_config(page_title="Resource Allocation", page_icon="🛏️", layout="wide")
theme.inject_global_css()
theme.page_header("🛏️", "Resource Allocation",
                   "Recommended allocation of beds, staff and ICU capacity based on current patient load.")

resources = resource_table()

cols = st.columns(len(resources))
for col, (_, r) in zip(cols, resources.iterrows()):
    utilization = r["Available"] / r["Capacity"]
    color = theme.RISK_HIGH if utilization < 0.15 else theme.RISK_MED if utilization < 0.4 else theme.RISK_LOW
    with col:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=r["Available"],
            number={"suffix": f" / {r['Capacity']}", "font": {"size": 22, "color": theme.NAVY}},
            gauge={
                "axis": {"range": [0, r["Capacity"]], "tickcolor": theme.MUTED},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "white", "borderwidth": 0,
            },
            title={"text": r["Resource"], "font": {"size": 14, "color": theme.MUTED}},
        ))
        fig.update_layout(height=190, margin=dict(t=40, b=0, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

st.write("")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("##### 📋 Allocation Plan")
st.dataframe(resources, use_container_width=True, hide_index=True)

for _, r in resources.iterrows():
    delta = r["Recommended Allocation"] - r["Available"]
    arrow = "🔺 increase" if delta > 0 else ("🔻 reduce" if delta < 0 else "▪️ hold")
    st.write(f"**{r['Resource']}** — {r['Available']} available / {r['Capacity']} capacity → "
             f"recommended **{r['Recommended Allocation']}** ({arrow} by {abs(delta)})")
    st.progress(min(1.0, float(r["Available"]) / float(r["Capacity"])))
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Recommended allocation is nudged upward for ICU capacity based on the current count of High-priority patients in the queue. "
           "A full mathematical optimization model can be plugged into `src/data.py::resource_table()`.")
theme.footer()
