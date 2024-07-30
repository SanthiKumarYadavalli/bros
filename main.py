import streamlit as st
import pandas as pd
import requests
import datetime
import numpy as np
from static.styles import CSS

IMAGE_URL = "https://raw.githubusercontent.com/pythonista69/r20/main/images/"
today = datetime.date.today()

# Extra styling
st.markdown(CSS, unsafe_allow_html=True)


# to retrieve data
@st.cache_data
def get_data():
    data = pd.read_csv("the_data.csv")
    data['DOB'] = pd.to_datetime(data['DOB'], format='%d/%m/%Y')
    data['PHONE'] = data['PHONE'].astype('str').replace('0', np.nan)
    return data


# GET image
@st.cache_data
def get_image(ID):
    res = requests.get(f"{IMAGE_URL}{ID}.jpg")
    return res.content if res.ok else IMAGE_URL + "not_found.jpg"


# GET birthday's info
def get_birthdays(data, date):
    birthdays = data[(data.DOB.dt.month == date.month) & (
                data.DOB.dt.day == date.day)]\
                .loc[:, ['ID', 'NAME', 'BRANCH']].reset_index(drop=True)
    birthdays.index += 1
    return birthdays


data = get_data()
tab1, tab2 = st.tabs(["Search", "Birthdays",])

# SEARCH_TAB
with tab1:
    # search box
    search_fields = ["ID", "NAME", "PHONE"]
    selected_field = st.radio("SEARCH BY", search_fields, index=0)
    selected_value = st.selectbox("Search", data[selected_field].dropna(),
                                  placeholder=f"Enter {selected_field}", index=None)
    # fetching data
    bro_data = None
    if selected_value:
        bro_data = data.query(f"{selected_field} == '{selected_value}'").iloc[0]

    # DISPLAYING DATA
    if bro_data is not None:
        st.subheader(bro_data['NAME'], divider="rainbow")
        col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
        bro_data.name = ""  # hide table header

        with col1:  # image col
            st.image(get_image(bro_data['ID']))

        with col2:  # details col
            cols = ['ID', 'GENDER', 'DOB', 'BRANCH', 'FATHER',
                    'CASTE', 'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE']
            display_df = bro_data[cols]
            display_df["DOB"] = display_df["DOB"].strftime("%d %B %Y")
            st.table(display_df)
            if bro_data.notna()["PHONE"]:
                st.link_button(":green[Whatsapp]",
                               f"https://wa.me/+91{bro_data.PHONE}")
        # BIRTHDAY BRO
        if bro_data['DOB'].month == today.month and bro_data['DOB'].day == today.day:
            st.balloons()


# BIRTHDAY TAB
with tab2:
    day = st.radio(label="When", options=['Yesterday', 'Today', 'Tomorrow'], index=1)
    delta = {"Yesterday": -1, "Today": 0, "Tomorrow": 1}
    birthdays = get_birthdays(data, today + datetime.timedelta(days=delta[day]))
    birthdays
