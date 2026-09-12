import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
import streamlit as st

from src import theme
from src.data import demand_series

st.set_page_config(page_title="Demand Prediction", page_icon="📈", layout="wide")
theme.inject_global_css()
theme.page_header("📈", "Hospital Demand Prediction",
                   "14-day forecast of incoming patients, bed demand and ICU demand.")

df = demand_series()

k1, k2, k3 = st.columns(3)
with k1:
    theme.kpi_card("Forecast Peak (Patients/day)", f"{int(df['Predicted Patients'].max())}")
with k2:
    theme.kpi_card("Peak Bed Demand", f"{int(df['Bed Demand'].max())}")
with k3:
    theme.kpi_card("Peak ICU Demand", f"{int(df['ICU Demand'].max())}")

st.write("")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("##### Patient Volume — Actual vs. Predicted")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["Date"], y=df["Actual Patients"], name="Actual",
                           mode="lines+markers", line=dict(color=theme.NAVY, width=3)))
fig1.add_trace(go.Scatter(x=df["Date"], y=df["Predicted Patients"], name="Predicted",
                           mode="lines+markers", line=dict(color=theme.TEAL, width=3, dash="dash")))
fig1.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### General Bed Demand")
    fig2 = go.Figure(go.Bar(x=df["Date"], y=df["Bed Demand"], marker_color=theme.BLUE))
    fig2.update_layout(height=260, margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### ICU Demand")
    fig3 = go.Figure(go.Bar(x=df["Date"], y=df["ICU Demand"], marker_color=theme.RISK_HIGH))
    fig3.update_layout(height=260, margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📄 View underlying forecast data"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.info("Forecast values are an illustrative sample trend until the team's dedicated time-series forecasting model is integrated (see `src/data.py`).")
theme.footer()
