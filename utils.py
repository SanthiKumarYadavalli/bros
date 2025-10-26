from collections import Counter, defaultdict
from string import ascii_lowercase, ascii_uppercase
import datetime
import requests
import streamlit as st
import pandas as pd
import joblib
# import face_recognition

pd.options.mode.copy_on_write = True
IMAGE_URL = "https://raw.githubusercontent.com/pythonista69/r20/main/images/"
DEFAULT_LAYOUT = dict(
    dragmode=False,
    hovermode=False,
    showlegend=False
)


def calculate_age(dob):
    today = datetime.date.today()
    return (today.year - dob.year - ((dob.month, dob.day) > (today.month, today.day)))


# to retrieve data
@st.cache_data
def get_data():
    data = joblib.load("data")
    data['AGE'] = data["DOB"].apply(calculate_age)
    data["IMG"] = data["ID"].apply(lambda x: f"{IMAGE_URL}{x}.jpg")
    return data


@st.cache_data
def get_famous_bros():
    return joblib.load("famousbros")


# GET image
@st.cache_data
def get_image(ID, serial=0):
    res = requests.get(f"{IMAGE_URL}/{ID}/{serial}.jpg")
    if not res.ok:
        res = requests.get(f"{IMAGE_URL}/{ID}/0.jpg")
        serial = 0
    if not res.ok:
        res = requests.get(f"{IMAGE_URL}/{ID}/not_found/0.jpg")
    return res.content, serial

# GET birthday's info
def get_birthdays(data, date):
    """get all bros whose birthday is on the given date"""
    birthdays = data[
        (data.DOB.dt.month == date.month) &
        (data.DOB.dt.day == date.day)
    ]
    wish = "Happy Birthday! ✨"
    birthdays["WhatsApp"] = birthdays["PHONE"].apply(
        lambda x: f"https://wa.me/91{x}?text={wish}"
    )
    birthdays = birthdays.loc[:, 
        ['IMG', 'NAME', 'BRANCH', "WhatsApp"]
    ].reset_index(drop=True)
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


def get_flames_1v1(s1, s2):
    """Simple 1v1 flames"""
    c1 = Counter(s1.lower())
    c2 = Counter(s2.lower())
    num = sum([abs(c1[x] - c2[x]) for x in ascii_lowercase]) - 1
    arr = [0, 1, 2, 3, 4, 5]
    i = 0
    while len(arr) > 1:
        i = (i + num) % len(arr)
        arr.pop(i)
    return arr[0], flame_map[arr[0]]


def get_flames_1vn(bro):
    """returns a dataframe of containing bro's opposite gender guys
    with a 'flame' column of flame of bro and them"""
    data = get_data()
    g = data[data['NAME'] == bro].iloc[0, 2]  # gender of bro
    them = data.loc[
        data["GENDER"] == ('FEMALE' if g == 'MALE' else 'MALE'),
        ['NAME', 'BRANCH']
    ]  # opposite gender bros
    them['flame'] = them.apply(
        lambda s1: get_flames_1v1(bro, s1["NAME"])[1],
        axis=1
    )
    them['flame'] = them['flame'].astype("category")
    them['flame'] = them['flame'].cat.set_categories(flame_map.values())
    return them


# @st.cache_data
# def get_flame_matrix():
#     data = get_data()
#     males = data.query("GENDER == 'MALE'")["NAME"].reset_index(drop=True)
#     females = data.query("GENDER == 'FEMALE'")["NAME"].reset_index(drop=True)
#     flame_matrix = np.zeros((len(males), len(females)))
#     for i, potta in males.items():
#         for j, potti in females.items():
#             flame_matrix[i][j] = get_flames_1v1(potta, potti)[0]

#     male_matrix = np.zeros((len(males), 6))
#     female_matrix = np.zeros((len(females), 6))
#     for i in range(flame_matrix.shape[0]):
#         vals, counts = np.unique(flame_matrix[i], return_counts=True)
#         vals = vals.astype(int)
#         for j in range(len(vals)):
#             male_matrix[i][vals[j]] = counts[j]

#     flame_matrix = flame_matrix.T
#     for i in range(flame_matrix.shape[0]):
#         vals, counts = np.unique(flame_matrix[i], return_counts=True)
#         vals = vals.astype(int)
#         for j in range(len(vals)):
#             female_matrix[i][vals[j]] = counts[j]

#     return male_matrix, female_matrix


@st.cache_data
def get_name_counts():
    """Returns subnames frequency and character frequency of all names"""
    freq_by_subname = defaultdict(int)
    freq_by_char = {x: 0 for x in ascii_uppercase}
    for name in get_data()["NAME"]:
        for sub in name.split()[1:]:
            if len(sub) > 1:
                freq_by_subname[sub] += 1
        for c in name:
            if c in freq_by_char:
                freq_by_char[c] += 1

    return (
        sorted(freq_by_subname.items(), key=lambda x: x[1])[::-1],
        list(freq_by_char.items())
    )


def get_bro_from_image(img, data: pd.DataFrame):
    """Predicts a bro from a image using face_recognition
    @param img: image file
    @param data: dataframe containing 'enc' column of face_encodings
    """
    data.rename(columns={"enc": "ENCODINGS"}, inplace=True)
    data.dropna(subset=["ENCODINGS"], inplace=True)  
    img = face_recognition.load_image_file(img)
    enc = face_recognition.face_encodings(img)
    if enc:
        data['DISTANCE'] = data["ENCODINGS"].apply(lambda e: face_recognition.face_distance([e], enc[0])[0])
        mindex = data["DISTANCE"].idxmin()
        return data.loc[mindex].to_dict()  # a dataframe containing the predicted bro in a single row
    # returns None if no face is detected
