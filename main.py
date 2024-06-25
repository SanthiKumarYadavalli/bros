import streamlit as st
import pandas as pd
import requests

@st.cache_data
def get_data():
    return pd.read_csv("the_data.csv")

data = get_data()

# search box
search = st.radio("SEARCH BY", ["ID", "NAME"], index=0)
id_, name = None, None
if search == 'ID':
    id_ = st.selectbox("ID NUMBER", data['ID'], placeholder="Enter Id", index=None)
else:
    name = st.selectbox("NAME", data['NAME'], placeholder='Enter Name', index=None)

# fetching data
bro_data = None
if id_:
    bro_data = data.query(f"ID == '{id_}'").iloc[0]
if name:
    bro_data = data.query(f"NAME == '{name}'").iloc[0]

# DISPLAYING DATA
col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
if bro_data is not None:
    bro_data.name = ""  # hide table header
    #image col
    with col1:
        res = requests.get(f"https://raw.githubusercontent.com/pythonista69/r20/main/images/{bro_data['ID']}.jpg")
        if res.ok:
            st.image(res.content)
        else:
            st.image("https://raw.githubusercontent.com/pythonista69/r20/main/images/not_found.jpg")
    #details col
    with col2:
        st.subheader(bro_data['NAME'], divider="rainbow")
        cols = ['ID', 'GENDER', 'DOB', 'BRANCH', 'FATHER', 'CASTE', 'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE']
        st.table(bro_data[cols])
        if bro_data.PHONE != 0:
            st.link_button(":green[Whatsapp]", f"https://wa.me/+91{bro_data.PHONE}")
    