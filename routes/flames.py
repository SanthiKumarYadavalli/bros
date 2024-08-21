import streamlit as st
import plotly.express as px
import utils

tab1, tab2, tab3 = st.tabs(["1 vs 1", "1 vs n", "record holders"])
data = utils.get_data()

# --- 1 v 1 ---
with tab1:
    bro = st.selectbox(
        "You", data['NAME'], 
        index=None, placeholder="Enter Your Name"
    )
    if bro:
        brogender = data.query(f"NAME == '{bro}'")["GENDER"].iloc[0]
        pronoun = ("He", "His") if brogender == "FEMALE" else ("She", "Her")
        bro2 = st.selectbox(
            pronoun[0],
            data[data["GENDER"] == ("FEMALE" if brogender == "MALE" else "MALE")]['NAME'],
            index=None, placeholder=f"Enter {pronoun[1]} Name"
        )

    if bro and bro2:
        num, text = utils.get_flames_1v1(bro, bro2)
        st.markdown(
            f"<p style='text-align: center; font-family: monospace; font-size:2rem'>{text}</p>",
            unsafe_allow_html=True
        )
        if num in [1, 3]:
            st.balloons()


# --- 1 v N --- 
with tab2:
    st.caption("Your name is going to be flamed with every one of your opposite gender.")
    bro = st.selectbox("Name", data['NAME'],
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
            color_discrete_map=dict(zip(counts['flame'], colors))
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


def display_records(data, col, maximum=True):
    """displays bros who are having max/min value in 'col' column"""
    top_element = data[col].max() if maximum else data[col].min()
    bros = data.loc[data[col] == top_element][["NAME", col]]
    c = "green" if maximum else "red"
    for i, row in bros.iterrows():
        if col[-1] == 'p':  # if col is a percentage column
            st.info(f"{row.iloc[0]} - :{c}[{round(row.iloc[1] * 100, 2)}%]")
        else:
            st.info(f"{row.iloc[0]} - :{c}[{row.iloc[1]}]")


with tab3:
    gc = data["GENDER"].value_counts()
    mc, fc = gc["MALE"], gc["FEMALE"]
    st.write(f"Boys' count: {mc}")
    st.write(f"Girls' count: {fc}")
    
    perc = lambda row: row.iloc[1] / (fc if row.iloc[0] == "MALE" else mc)
    for i, x in enumerate("flames"):
        pcol = x + 'p'  # percentage column
        data[pcol] = data[["GENDER", x]].apply(perc, axis=1)
        st.subheader(utils.flame_map[i])
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.write("Maximum by percentage")
            display_records(data, pcol, maximum=True)
            if x != 's':
                st.write("Minimum by percentage")
                display_records(data, pcol, maximum=False)
        
        with col2:
            st.write("Maximum by count")
            display_records(data, x, maximum=True)
            if x != 's':
                st.write("Minimum by count")
                display_records(data, x, maximum=False)
         
    st.write(f"Students with zero siblings: :red[{data.loc[data[x] == 0]['NAME'].count()}]")
