import streamlit as st
import plotly.express as px
import utils

tab1, tab2, tab3 = st.tabs(["1 vs 1", "1 vs n", "records"])
data = utils.get_data()


with tab1:
    bro = st.selectbox(
        "You", data['NAME'], 
        index=None, placeholder="Enter Your Name"
    )
    if bro:
        brogender = data.query(f"NAME == '{bro}'")["GENDER"].iloc[0]
        bro2 = st.selectbox(
            "Them", 
            data[data["GENDER"] == ("FEMALE" if brogender == "MALE" else "MALE")]['NAME'],
            index=None, placeholder="Enter their Name"
        )

    if bro and bro2:
        num, text = utils.get_flames_1v1(bro, bro2)
        st.markdown(
            f"<p style='text-align: center; font-family: monospace; font-size:2rem'>{text}</p>",
            unsafe_allow_html=True
        )
        if num in [1, 3]:
            st.balloons()


with tab2:
    bro = st.selectbox("name", data['NAME'],
                       index=None, placeholder="Enter Your Name")
    if bro:
        them = utils.get_flames_1vn(bro)
        groups = them.groupby('flame', observed=True)
        counts = them['flame'].value_counts().sort_index().reset_index()
        colors = ["#9ADCFF", "#FF8AAE", "#756AB6", "#FAF3F0", "#FF4040","#ECEE81"]
        fig = px.bar(
            counts,
            x='flame',
            y='count',
            text_auto=True,
            color='flame',
            color_discrete_map={w:c for w, c in zip(counts['flame'], colors)}
        )
        fig.update_traces(
            textposition='outside',
            hovertemplate="%{x}",
        )
        fig.update_layout(
            **utils.DEFAULT_LAYOUT,
            xaxis_title='',
            yaxis_title='count',
        )
        st.caption("Click a bar to see who they are!")
        select = st.plotly_chart(fig, on_select='rerun')
        
        if select["selection"]["points"]:
            selected = select['selection']["points"][0]['x']
            selected_bros = groups.get_group(selected)
            
            st.subheader("Your " + selected)
            st.dataframe(selected_bros[["NAME", "BRANCH"]], hide_index=True, use_container_width=True)


with tab3:
    st.write("coming soon")