from itertools import product
import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()
st.write("Here, You will uncover hidden truths that lie within the data")
st.write("First, choose an attribute")
column = st.selectbox("Attribute", ["Names", "Birthdays", "Place"], index=None)

if column == "Names":
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        st.subheader("Longest Name")
        longest_name = data.iloc[data["NAME"].str.len().idxmax()]['NAME']
        st.info(f"{longest_name} - :green[{len(longest_name)} chars]")

    with col2:
        st.subheader("Shortest Name")
        shortest_name = data.iloc[data["NAME"].str.len().idxmin()]['NAME']
        st.info(f"{shortest_name} - :green[{len(shortest_name)} chars]")

    # --- Name freq ---
    st.subheader("Top Names")
    st.write("This shows count of top subnames.")
    name_freq, char_freq = utils.get_name_counts()
    top_names = name_freq[:20]
    fig = px.bar(
        x=[name for name, _ in top_names],
        y=[count for _, count in top_names],
        text_auto=True
    )
    fig.update_traces(textposition="outside", textfont_size=14)
    fig.update_layout(
        **utils.DEFAULT_LAYOUT, 
        xaxis_title='', 
        yaxis_title='',
        yaxis_showgrid=False
    )
    st.plotly_chart(fig)

    st.subheader("Character Count")
    st.write("This shows count of each character in all names combined.")
    fig = px.bar(
        x=[name for name, _ in char_freq],
        y=[count for _, count in char_freq],
        text_auto=True
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        **utils.DEFAULT_LAYOUT, 
        xaxis_title='', 
        yaxis_title='',
        yaxis_showgrid=False
    )
    st.plotly_chart(fig)
    
    
elif column == "Birthdays":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Oldest")
        idx = data["DOB"].idxmin()
        st.info(
            f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])} years]')
    with col2:
        st.subheader("Youngest")
        idx = data["DOB"].idxmax()
        st.info(
            f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])} years]')

    st.divider()

    # --- Birthday count ---
    st.subheader("Birthday count")
    st.write("Let's check out how many birthdays fall in a time range")

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
        textfont_size=14,
        hovertemplate="%{y}<extra></extra><br>%{x}"
    )
    fig.update_layout(
        dragmode=False,
        showlegend=how == "Year-Month",
        hovermode='closest' if how == "Year-Month" else False
    )
    st.plotly_chart(fig)


    # --- Age Count ---
    st.subheader("Age count")
    st.write("This counts ages of everyone.")
    ages = data['AGE'].value_counts().reset_index()
    fig = px.pie(ages, values='count', names='AGE', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+value')
    st.plotly_chart(fig)


elif column == "Place":
    st.subheader("Count by District and ...")
    data.loc[1093, 'MANDAL'] = 'BANGLORE'
    vs = st.selectbox("and?", ["MANDAL", "GENDER"])
    fig = px.sunburst(data, path=["DISTRICT", vs], width=800, height=800)
    fig.update_traces(
        hovertemplate="Count: %{value}"
    )
    fig.update_layout(
        dragmode=False,
        hoverlabel={"font_size": 20}
    )

    st.plotly_chart(fig)


if column:
    st.caption("More to come.")
