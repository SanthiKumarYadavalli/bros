from collections import Counter
from string import ascii_lowercase
from itertools import product
import datetime
import requests
import streamlit as st
import pandas as pd
import joblib

pd.options.mode.copy_on_write = True
IMAGE_URL = "https://raw.githubusercontent.com/pythonista69/r20/main/images/"
DEFAULT_LAYOUT = dict(
    dragmode=False,
    hovermode=False,
    showlegend=False
)
today = datetime.date.today()


def calculate_age(dob):
    return (today.year - dob.year - ((dob.month, dob.day) > (today.month, today.day)))


# to retrieve data
@st.cache_data
def get_data():
    data = joblib.load("data")
    data['AGE'] = data["DOB"].apply(calculate_age)
    return data


# GET image
@st.cache_data
def get_image(ID):
    res = requests.get(f"{IMAGE_URL}{ID}.jpg")
    return res.content if res.ok else IMAGE_URL + "not_found.jpg"


# GET birthday's info
def get_birthdays(data, date):
    birthdays = data[
        (data.DOB.dt.month == date.month) &
        (data.DOB.dt.day == date.day)
    ]
    wish = "Happy Birthday! ✨"
    birthdays["WhatsApp"] = birthdays["PHONE"].apply(
        lambda x: f"https://wa.me/91{x}?text={wish}")
    birthdays["IMG"] = birthdays["ID"].apply(lambda x: f"{IMAGE_URL}{x}.jpg")
    birthdays = birthdays.loc[:, ['IMG', 'NAME',
                                  'BRANCH', "WhatsApp"]].reset_index(drop=True)
    birthdays.index += 1
    return birthdays


flame_map = {
    0: "Friends",
    1: "Lovers",
    2: "Affection",
    3: "Marriage",
    4: "Enemies",
    5: "Siblings",
}


def get_flame_text(s1, s2):
    c1 = Counter(s1.lower())
    c2 = Counter(s2.lower())
    num = sum([abs(c1[x] - c2[x]) for x in ascii_lowercase]) - 1
    arr = [0, 1, 2, 3, 4, 5]
    i = 0
    while len(arr) > 1:
        i = (i + num) % len(arr)
        arr.pop(i)
    return arr[0], flame_map[arr[0]]


def get_flame_bros(bro):
    data = get_data()
    g = data[data['NAME'] == bro].iloc[0, 2]
    them = data.loc[
        data["GENDER"] == ('FEMALE' if g == 'MALE' else 'MALE'),
        ['NAME', 'BRANCH']
    ]
    them['flame'] = them.apply(
        lambda s1: get_flame_text(bro, s1["NAME"])[1], axis=1)
    them['flame'] = them['flame'].astype("category")
    them['flame'] = them['flame'].cat.set_categories(flame_map.values())
    return them
