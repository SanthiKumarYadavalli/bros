import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()

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