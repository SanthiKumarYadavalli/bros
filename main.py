import streamlit as st
from styles import CSS

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/search.py", title="Search", icon="⚡"),
    st.Page("pages/birthdays.py", title="Birthdays", icon="🩷"),
    st.Page("pages/fun.py", title="Fun", icon="🔥"),
    st.Page("pages/insights.py", title="Insights", icon="☀️")
])
pg.run() 