import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()

def distribution_chart():
    st.subheader("No. of Students by District and ...")
    vs = st.selectbox("and?", ["MANDAL", "GENDER"])
    fig = px.sunburst(data, path=["DISTRICT", vs], width=800, height=800)
    fig.update_traces(
        hovertemplate="%{label}<br>Count: %{value}"
    )
    fig.update_layout(
        dragmode=False,
        hoverlabel={"font_size": 20}
    )
    st.plotly_chart(fig)


def render_page():
    distribution_chart()