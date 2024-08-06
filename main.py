import streamlit as st

pg = st.navigation([
    st.Page("pages/serious.py", title="Serious", icon="✨"),
    st.Page("pages/fun.py", title="Fun", icon="🔥"),
    st.Page("pages/insights.py", title="Insights", icon="📊")
])
pg.run()