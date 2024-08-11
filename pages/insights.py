import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()
col1, col2 = st.columns(2, vertical_alignment='center')
with col1:
    st.subheader("Longest Name")
    longest_name = data.iloc[data["NAME"].str.len().idxmax()]['NAME']
    st.info(f"{longest_name} - :green[{len(longest_name.replace(' ', ''))}]")

with col2:
    st.subheader("Shortest Name")
    shortest_name = data.iloc[data["NAME"].str.len().idxmin()]['NAME']
    st.info(f"{shortest_name} - :green[{len(shortest_name.replace(' ', ''))}]")
    
col1, col2 = st.columns(2)
with col1:
    st.subheader("Oldest")
    idx = data["DOB"].idxmin()
    st.info(f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])}y]')
with col2:
    st.subheader("Youngest")
    idx = data["DOB"].idxmax()
    st.info(f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])}y]')

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

st.subheader("Age count")
age_count = utils.get_ages(data['DOB'])
st.plotly_chart(px.bar(age_count))

st.caption("More to come.")