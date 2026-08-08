import utils
import streamlit as st

data = utils.get_data()


def get_leaderboard_data(gpa_type, sem):
    sgpa_cols = utils.SEMESTER_COLS
    leaderboard_data = data[["ID", "NAME", "BRANCH", "subjects", *sgpa_cols]]
    leaderboard_data = leaderboard_data.dropna(subset=sgpa_cols, how="any")
    leaderboard_data["gpa_calculated"] = leaderboard_data.apply(
        lambda row: utils.calculate_gpa_from_subjects(row, sem, "cgpa" if gpa_type else "sgpa"), axis=1
    )
    leaderboard_data.sort_values(by="gpa_calculated", ascending=False, inplace=True)
    leaderboard_data["CGPA"] = leaderboard_data["gpa_calculated"].round(2)
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
    branch_dropdown_options = list(data["BRANCH"].unique())
    branch_dropdown_options.remove("GONE")
    branch_filter = st.selectbox(
        "Branch",
        branch_dropdown_options,
        index=None, 
        placeholder="Select a branch"
    )
    if branch_filter:
        gpa_type = st.radio(
            "GPA Type",
            options=["Cumulative (CGPA)", "Semester (SGPA)"],
            index=0,
            horizontal=True,
        )
        sem = st.select_slider(
            "Semester",
            options=utils.SEMESTER_COLS,
            value=utils.SEMESTER_COLS[-1],
            format_func=lambda x: x.upper(),
        )
        leaderboard_data = get_leaderboard_data(gpa_type == "Cumulative (CGPA)", sem)
        leaderboard_data = leaderboard_data[leaderboard_data["BRANCH"] == branch_filter]
        add_rank_column(leaderboard_data)
        st.dataframe(
            leaderboard_data[["RANK", "ID", "NAME", "CGPA"]],
            width="stretch",
            hide_index=True
        )
