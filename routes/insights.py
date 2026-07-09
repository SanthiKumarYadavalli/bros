import streamlit as st
from routes.insights import (
    gpa,
    name,
    dob,
    place,
    leaderboard
)

attribute_module_map = {
    "Leaderboard": leaderboard,
    "GPA": gpa,
    "Names": name,
    "Birthdays": dob,
    "Place": place,
}

tabs = st.tabs(list(attribute_module_map.keys()))
for tab, title in zip(tabs, attribute_module_map.keys()):
    with tab:
        attribute_module_map[title].render_page()
