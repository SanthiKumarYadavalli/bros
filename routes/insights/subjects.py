import utils
import streamlit as st
import pandas as pd

data = utils.get_data()

def get_subjects_df():
    df = data[["ID", "NAME", "BRANCH", "subjects"]]
    df = df.dropna(subset=["subjects"], how="any")
    exploded = df.explode("subjects", ignore_index=True)
    subjects_data = pd.json_normalize(exploded["subjects"])
    df = pd.concat([exploded, subjects_data], axis=1)
    df.drop(columns=["subjects", "first_attempt"], inplace=True)
    return df


def render_page():
    st.subheader("Grades", divider="blue")
    id_or_name_filter = st.selectbox(
        "Bro",
        options=(data["ID"].unique().tolist() + data["NAME"].unique().tolist()),
        index=None,
        placeholder="Select an ID or Name",
    )
    if id_or_name_filter:
        df = get_subjects_df()
        df = df[(df["ID"] == id_or_name_filter) | (df["NAME"] == id_or_name_filter)]
        df["points"] = df["grade"].map(lambda x: utils.GRADE_TO_POINTS_MAP.get(x, 0)) * df["credit"]
        st.dataframe(df[["year", "sem", "subject", "credit", "grade"]], width="stretch", hide_index=True)
        total_points = int(df["points"].sum())
        total_credits = int(df["credit"].sum())
        st.write(f"Total Points: {total_points} / {total_credits * 10} ({total_points / total_credits * 10:.2f}%)")
