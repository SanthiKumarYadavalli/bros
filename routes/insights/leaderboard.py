import utils
import streamlit as st

data = utils.get_data()


def get_leaderboard_data():
    sgpa_cols = [
        "e1sem1", "e1sem2", "e2sem1", "e2sem2",
        "e3sem1", "e3sem2", "e4sem1", "e4sem2"
    ]
    leaderboard_data = data[["ID", "NAME", "BRANCH", "subjects", "CGPA", *sgpa_cols]]
    leaderboard_data = leaderboard_data.dropna(subset=sgpa_cols, how="any")
    leaderboard_data["cgpa_calculated"] = leaderboard_data.apply(
        utils.calculate_cgpa_from_subjects, axis=1
    )
    leaderboard_data.sort_values(by="cgpa_calculated", ascending=False, inplace=True)
    return leaderboard_data


def add_rank_column(leaderboard_data):
    medals = {
        "1": "🥇", "2": "🥈", "3": "🥉", "4": "4️⃣", "5": "5️⃣",
        "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣", "10": "🔟"
    }
    leaderboard_data.insert(
        0,
        "RANK",
        [medals.get(str(i), f"#{i}") for i in range(1, len(leaderboard_data) + 1)]
    )


def render_page():
    leaderboard_data = get_leaderboard_data()
    branch_filter = st.selectbox("BRANCH", list(leaderboard_data["BRANCH"].unique()), index=None, placeholder="Select a branch")
    if branch_filter:
        leaderboard_data = leaderboard_data[leaderboard_data["BRANCH"] == branch_filter]
        add_rank_column(leaderboard_data)
        st.dataframe(
            leaderboard_data[["RANK", "ID", "NAME", "CGPA"]],
            width="stretch",
            hide_index=True
        )
