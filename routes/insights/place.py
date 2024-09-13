import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()

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