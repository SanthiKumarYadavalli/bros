from collections import Counter
from string import ascii_lowercase
from itertools import product
import datetime
import os
import requests
import streamlit as st
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DATA_URL = os.getenv("DATA_URL")
IMAGE_URL = os.getenv("IMAGE_URL")
today = datetime.date.today()


# to retrieve data
@st.cache_data
def get_data():
    data = pd.read_csv(DATA_URL)
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
    them['flame'] = them.apply(lambda s1: get_flame_text(bro, s1["NAME"])[1], axis=1)
    them['flame'] = them['flame'].astype("category")
    them['flame'] = them['flame'].cat.set_categories(flame_map.values())
    return them


date_formats = {
    "Year": "%Y",
    "Month": "%b",
    "Day": "%a",
    "Year-Month": "%Y-%b"
}


@st.cache_data
def get_birthday_count(dob, how):
    """returns a DataFrame of count of birthdays based on 'how'"""
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    years = sorted(dob.dt.strftime("%Y").unique())
    order = {
        "Month": months,
        "Day": days,
        "Year-Month": ["-".join(p) for p in product(years, months)]
    }
    dob = dob.dt.strftime(date_formats[how]).astype('category')
    if how in order:
        dob = dob.cat.set_categories(order[how], ordered=True)
    return dob.value_counts().rename_axis(how).reset_index()


def get_ages(dobs):
    """return a series of count of ages"""
    age_count = (today.year - dobs.dt.year + ((dobs.dt.month < today.month) & (dobs.dt.day < today.day)).astype(int)).value_counts()
    age_count.index.name = 'Age'
    return age_count

def calculate_age(dob):
    return (today.year - dob.year + ((dob.month < today.month) and (dob.day < today.day)))