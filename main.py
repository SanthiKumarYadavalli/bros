import streamlit as st
import pandas as pd
import requests
from static.styles import CSS
import datetime

# Extra styling
st.markdown(CSS, unsafe_allow_html=True)

# to retrieve data


@st.cache_data
def get_data():
    data = pd.read_csv("the_data.csv")
    data['DOB'] = pd.to_datetime(data['DOB'], format='%d/%m/%Y')
    return data


# GET birthday's info
def get_birthdays(data, date):
    birthdays = data[(data.DOB.dt.month == date.month) & (
        data.DOB.dt.day == date.day)].loc[:, ['ID', 'NAME', 'BRANCH']].reset_index(drop=True)
    birthdays.index += 1
    return birthdays


data = get_data()
today = datetime.date.today()

# search box
search = st.radio("SEARCH BY", ["ID", "NAME"], index=0)
id_, name = None, None
if search == 'ID':
    id_ = st.selectbox(
        "ID NUMBER", data['ID'], placeholder="Enter Id", index=None)
else:
    name = st.selectbox("NAME", data['NAME'],
                        placeholder='Enter Name', index=None)

# fetching data
bro_data = None
if id_:
    bro_data = data.query(f"ID == '{id_}'").iloc[0]
if name:
    bro_data = data.query(f"NAME == '{name}'").iloc[0]


# DISPLAYING DATA
if bro_data is not None:
    if bro_data['DOB'].month == today.month and bro_data['DOB'].day == today.day:  # BIRTHDAY BRO
        st.balloons()
    st.subheader("Profile", divider='rainbow')
    col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
    bro_data.name = ""  # hide table header
    # image col
    with col1:
        res = requests.get(
            f"https://raw.githubusercontent.com/pythonista69/r20/main/images/{bro_data['ID']}.jpg")
        if res.ok:
            st.image(res.content)
        else:
            st.image(
                "https://raw.githubusercontent.com/pythonista69/r20/main/images/not_found.jpg")
    # details col
    with col2:
        st.subheader(bro_data['NAME'], divider="rainbow")
        cols = ['ID', 'GENDER', 'DOB', 'BRANCH', 'FATHER',
                'CASTE', 'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE']
        st.table(bro_data[cols])
        if bro_data.PHONE != 0:
            st.link_button(":green[Whatsapp]",
                           f"https://wa.me/+91{bro_data.PHONE}")


tab1, tab2 = st.tabs(["Birthday's", "Facts",])

# Birthday's tab
with tab1:
    day = st.radio(label="By", options=[
                   'Yesterday', 'Today', 'Tomorrow'], index=1)
    if day == 'Yesterday':
        birthdays = get_birthdays(data, today - datetime.timedelta(days=1))
    elif day == 'Today':
        birthdays = get_birthdays(data, today)
    else:
        birthdays = get_birthdays(data, today + datetime.timedelta(days=1))
    birthdays
