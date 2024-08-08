import streamlit as st
import plotly.express as px
import utils

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
birthday_frame = utils.get_birthday_frame(data["DOB"])
col = st.selectbox("By", birthday_frame.columns)
df = birthday_frame[col].value_counts()
color = df.index.str.slice(0, 4) if col == "Year-Month" else None
st.bar_chart(df)
