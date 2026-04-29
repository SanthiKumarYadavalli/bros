import importlib
import sys
import streamlit as st

attribute_module_map = {
    "Names": "name",
    "Birthdays": "dob",
    "Place": "place",
    "GPA": "gpa"
}

st.write("Choose an attribute")
selected_attr = st.selectbox("Attribute", attribute_module_map.keys(), index=None)
st.divider()

if selected_attr:
    module = attribute_module_map[selected_attr]
    sys.modules.pop(f"routes.insights.{module}", "")
    importlib.import_module(f"routes.insights.{module}")
    st.caption("More to come.")
