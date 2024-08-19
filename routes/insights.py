from itertools import product
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
    st.info(
        f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])}y]')
with col2:
    st.subheader("Youngest")
    idx = data["DOB"].idxmax()
    st.info(
        f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])}y]')

st.divider()

st.subheader("Birthday count")

dobs = data["DOB"]
date_formats = {
    "Year": "%Y",
    "Month": "%b",
    "Day": "%a",
    "Year-Month": "%Y-%b"
}
months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
years = sorted(dobs.dt.strftime("%Y").unique())
order = {
    "Year": years,
    "Month": months,
    "Day": days,
    "Year-Month": ["-".join(p) for p in product(years, months)]
}

how = st.selectbox("By", date_formats.keys())
counts = dobs.dt.strftime(
    date_formats[how]).value_counts().rename_axis(how).reset_index()
fig = px.bar(
    data_frame=counts,
    x=how,
    y="count",
    color=counts[how].str.slice(0, 4) if how == "Year-Month" else None,
    category_orders={how: order[how]},
    text_auto=True,
)
fig.update_traces(
    textposition="outside",
    hovertemplate="%{y}<extra></extra><br>%{x}"
)
fig.update_layout(
    dragmode=False,
    showlegend=how == "Year-Month",
    hovermode='closest' if how == "Year-Month" else False
)
st.plotly_chart(fig)

# Age Count
st.subheader("Age count")
fig = px.bar(data['AGE'].value_counts(), text_auto=True)
fig.update_traces(
    textposition='outside',
)
fig.update_layout(
    xaxis_title='Age',
    yaxis_title='count',
    **utils.DEFAULT_LAYOUT
)
st.plotly_chart(fig)


st.caption("More to come.")
