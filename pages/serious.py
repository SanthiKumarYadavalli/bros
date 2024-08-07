import datetime
import streamlit as st
import utils

data = utils.get_data()
today = datetime.date.today()
tab1, tab2 = st.tabs(["Search", "Birthdays",])

# SEARCH_TAB
with tab1:
    # search box
    search_fields = ["ID", "NAME", "PHONE"]
    selected_field = st.radio("SEARCH BY", search_fields, index=0)
    selected_value = st.selectbox(
        "Search", data[selected_field].dropna(),
        placeholder=f"Enter {selected_field}", index=None
    )
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
            st.image(utils.get_image(bro_data['ID']))

        with col2:  # details col
            cols = [
                'ID', 'GENDER', 'DOB', 'BRANCH', 'FATHER', 'MOTHER', 'CASTE', 
                'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE', 'Parent', 
                'BLOOD GROUP', 'ADDRESS', 'CGPA']
            display_df = bro_data[cols]
            display_df["DOB"] = display_df["DOB"].strftime("%d %B %Y")
            st.table(display_df)
            if bro_data.notna()["PHONE"]:
                st.link_button(
                    ":green[Whatsapp]",
                    f"https://wa.me/+91{bro_data.PHONE}"
                )
                
        # BIRTHDAY BRO
        if bro_data['DOB'].month == today.month and bro_data['DOB'].day == today.day:
            st.balloons()


# BIRTHDAY TAB
with tab2:
    day = st.radio(label="When", options=['Yesterday', 'Today', 'Tomorrow'], index=1)
    delta = {"Yesterday": -1, "Today": 0, "Tomorrow": 1}
    birthdays = utils.get_birthdays(data, today + datetime.timedelta(days=delta[day]))
    birthdays
