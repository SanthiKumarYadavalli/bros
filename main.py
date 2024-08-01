import streamlit as st

pg = st.navigation([
    st.Page("pages/serious.py", title="Serious", icon=":material/home:"),
    st.Page("pages/fun.py", title="Fun", icon=":material/favorite:")
])
pg.run()