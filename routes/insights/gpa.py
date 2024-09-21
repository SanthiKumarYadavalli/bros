import re
import streamlit as st
import plotly.express as px
import numpy as np
import utils

data = utils.get_data()

#_____________________________LINE_CHART___________________________________

st.subheader("SGPA Line Chart", divider="red")
st.write("Enter your name or id to get your chart")
gpa_cols = list(filter(lambda x: re.match("(p|e)\dsem\d", x), data.columns))
gpa_cols.sort(key=lambda x: x[0] == 'e')  # p comes before e
gpa_df = data[["ID", "NAME"] + gpa_cols]
gpa_df = gpa_df.dropna()
q = st.selectbox("Name or ID", gpa_df.ID.to_list() + gpa_df.NAME.to_list(),
                 placeholder="Enter Name or ID", index=None)
if not q:
    bro = gpa_df[gpa_cols].mean().round(2).reset_index()
    bro.rename(columns={"index": "sem", 0: "gpa"}, inplace=True)
    title = "Average GPAs"
else:
    nameorid = "ID" if q.startswith("R20") else "NAME"
    bro = gpa_df.loc[gpa_df[nameorid] == q, gpa_cols]
    bro = bro.melt(var_name="sem", value_name="gpa")
    title = "Your SGPAs"
bro['p_or_e'] = bro['sem'].str.slice(0, 1)
fig = px.line(bro, x="sem", y="gpa", text="gpa", title=title)
fig.update_traces(
    textposition="top left",
    hovertemplate="<extra></extra>%{y}",
)
fig.update_layout(
    dragmode=False,
    showlegend=False,
    hovermode="x unified",
    hoverlabel={"font_size": 15},
    yaxis_range=(3.5, 10.5)
)
st.plotly_chart(fig)

#___________________________DISTRIBUTION_________________________________

st.subheader("CGPA Distribution", divider="violet")
all_b = list(data["BRANCH"].unique())
all_b.remove("GONE")
bramches = st.multiselect("branch", all_b, 
                      placeholder="Select a bramch")
interval = st.selectbox("interval size", [1, 0.5], placeholder="select interval")
if not bramches:
    bramches = ["ALL"]
count_map = {}
for b in bramches:
    bramch_bros = data.query(f"BRANCH == @b") if b != 'ALL' else data
    histdata = np.histogram(bramch_bros.CGPA, range=[0, 10], bins=int(10//interval))
    count_map[b] = histdata[0]
    ticks = histdata[1]
    
fig = px.bar(
    data_frame=count_map,
    title=" & ".join(bramches) if bramches else "ALL R20",
    text_auto=True,
    y=bramches
)
fig.update_traces(
    hovertemplate="<br>%{x}<extra></extra><br>%{y}"
)
fig.update_layout(
    dragmode=False,
    xaxis_ticktext=[f"{ticks[i]} - {ticks[i + 1]}" for i in range(len(ticks) - 1)], 
    xaxis_tickvals=ticks * int(10 // (interval * 10)),
    xaxis_title="CGPA",
    yaxis_title="count",
    hoverlabel=dict(font={"size": 15})
)
st.plotly_chart(fig)
