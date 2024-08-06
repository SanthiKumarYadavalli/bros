import streamlit as st
import utils
import datetime

data = utils.get_data()
st.subheader("Longest Name")
st.success(data.iloc[data["NAME"].str.len().idxmax()]['NAME'])

st.subheader("Shortest Name")
st.info(data.iloc[data["NAME"].str.len().idxmin()]['NAME'])

st.subheader("Oldest")
st.success(data.iloc[data["DOB"].idxmin()]["NAME"])

st.subheader("Youngest")
st.info(data.iloc[data["DOB"].idxmax()]["NAME"])

st.divider()

st.subheader("Birthday count")
frmt = {"Year": "%Y", "Month": "%b", "Day": "%a", "Year-Month": "%Y-%b"}
how = st.selectbox("By", frmt.keys())
st.bar_chart(data["DOB"].dt.strftime(frmt[how]).value_counts())

