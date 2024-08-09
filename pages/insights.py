import streamlit as st
import utils

data = utils.get_data()
col1, col2 = st.columns(2, vertical_alignment='center')
with col1:
    st.subheader("Longest Name")
    st.info(data.iloc[data["NAME"].str.len().idxmax()]['NAME'])
with col2:
    st.subheader("Shortest Name")
    st.info(data.iloc[data["NAME"].str.len().idxmin()]['NAME'])
    
col1, col2 = st.columns(2)
with col1:
    st.subheader("Oldest")
    st.info(data.iloc[data["DOB"].idxmin()]["NAME"])
with col2:
    st.subheader("Youngest")
    st.info(data.iloc[data["DOB"].idxmax()]["NAME"])

st.divider()

st.subheader("Birthday count")
how = st.selectbox("By", utils.date_formats.keys())
df = utils.get_birthday_count(data["DOB"], how)
if how == "Year-Month":
    df["color"] = df[how].str.slice(0, 4)
st.bar_chart(
    data=df, 
    x=how, 
    y='count', 
    color='color' if 'color' in df.columns else None
)

st.caption("More to come.")