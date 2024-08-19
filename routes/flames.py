import streamlit as st
import plotly.express as px
import utils

tab1, tab2 = st.tabs(["Flames", "🔥"])
data = utils.get_data()
with tab1:
    bro = st.selectbox("You", data[data["GENDER"] == "MALE"]
                       ['NAME'], index=None, placeholder="Enter Your Name")
    fofa = st.selectbox("Her", data[data["GENDER"] == "FEMALE"]
                        ['NAME'], index=None, placeholder="Enter Her Name")

    if bro and fofa:
        num, text = utils.get_flame_text(bro, fofa)
        st.markdown(
            f"<p style='text-align: center; font-family: monospace; font-size:2rem'>{text}</p>",
            unsafe_allow_html=True
        )
        if num in [1, 3]:
            st.balloons()

with tab2:
    bro = st.selectbox("name", data['NAME'],
                       index=None, placeholder="Enter Your Name")
    flame = st.selectbox("flame", utils.flame_map.values(), index=1)
    if bro:
        them = utils.get_flame_bros(bro)
        groups = them.groupby('flame', observed=True)
        try:
            selected = groups.get_group(flame).drop(
                'flame', axis=1).reset_index(drop=True)
            selected.index += 1
        except KeyError:
            selected = None
        st.dataframe(selected)

        # header ?
        counts = them['flame'].value_counts().reset_index()
        fig = px.bar(counts,
                     x='flame',
                     y='count',
                     text_auto=True,
                     category_orders={'flame': ['Friends', 'Lovers', 'Affection', 'Marriage', 'Enemies', 'Siblings']}
        )
        fig.update_traces(
            textposition='outside'
        )
        fig.update_layout(
            **utils.DEFAULT_LAYOUT,
            xaxis_title='',
            yaxis_title='count',
        )
        st.plotly_chart(fig)
