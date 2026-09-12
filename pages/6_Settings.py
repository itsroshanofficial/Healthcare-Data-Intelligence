import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from src import theme
from src.data import priority_counts, SELECTED_MODEL, MODEL_LEADERBOARD

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
theme.inject_global_css()
theme.page_header("⚙️", "Settings", "App information, dataset details and cache controls.")

counts = priority_counts()
model_row = MODEL_LEADERBOARD[MODEL_LEADERBOARD["Model"] == SELECTED_MODEL].iloc[0]

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### ℹ️ Application Info")
    st.write(f"**App name:** Healthcare Data Intelligence")
    st.write(f"**Active model:** {SELECTED_MODEL} (Accuracy {model_row['Accuracy']:.1%}, ROC-AUC {model_row['ROC-AUC']:.3f})")
    st.write(f"**Patients in current dataset:** {counts['Total']:,}")
    st.write("**Theme:** Light (Navy / Teal)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 🗄️ Data &amp; Cache")
    st.write("Patient data and charts are cached for speed. If the underlying CSV or model files change, refresh the cache below.")
    if st.button("🔄 Clear cached data"):
        st.cache_data.clear()
        st.success("Cache cleared — data will reload on next page visit.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### 📚 Dataset Source")
    st.write("**Dataset:** Diabetes 130-US Hospitals for Years 1999–2008")
    st.write("**Target:** 30-day readmission (`readmitted_30`)")
    st.write("**Split strategy:** Patient-level train/test split (80/20) to avoid data leakage")
    st.write("See `documentation/ML_RESULTS.md` for the full methodology.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("##### ⚠️ Important Disclaimer")
    st.warning(
        "This is a decision-support **prototype**, not a certified medical "
        "device. Predictions and priority thresholds are project-defined and "
        "must be validated by qualified clinicians before any real-world use. "
        "Do not upload identifiable patient data to this app or its GitHub repository."
    )
    st.markdown('</div>', unsafe_allow_html=True)

theme.footer()
