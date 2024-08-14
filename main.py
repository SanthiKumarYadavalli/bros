import streamlit as st
from styles import CSS

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("sections/search.py", title="Search", icon="⚡"),
    st.Page("sections/birthdays.py", title="Birthdays", icon="🩷"),
    st.Page("sections/fun.py", title="Fun", icon="🔥"),
    st.Page("sections/insights.py", title="Insights", icon="☀️")
])
pg.run() 