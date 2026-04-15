import streamlit as st
from styles import CSS

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

pg = st.navigation({
    "Serious": [
        st.Page("routes/search.py", title="Search", icon="⚡"),
        st.Page("routes/birthdays.py", title="Birthdays", icon="🩷"),
        st.Page("routes/insights.py", title="Insights", icon="☀️")
    ],
    "Fun": [
        st.Page("routes/flames.py", title="Flames", icon="🔥"),
        st.Page("routes/cheese.py", title="Smile", icon="🐗")
    ],
    "Chat": [
        st.Page("routes/chat.py", title="Chat", icon="💬"),
    ],
})
pg.run() 