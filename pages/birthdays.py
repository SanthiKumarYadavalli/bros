import streamlit as st
import datetime
import utils

data = utils.get_data()
today = datetime.date.today()

day = st.radio(label="When", options=['Yesterday', 'Today', 'Tomorrow'], index=1)
delta = {"Yesterday": -1, "Today": 0, "Tomorrow": 1}
birthdays = utils.get_birthdays(data, today + datetime.timedelta(days=delta[day]))
if delta[day] != 0:
    birthdays = birthdays.drop("WhatsApp", axis=1)
ret = st.dataframe(
    birthdays,
    use_container_width=True,
    hide_index=True,
    column_config={
        "WhatsApp": st.column_config.LinkColumn(display_text="Wish Them!"),
        "IMG": st.column_config.ImageColumn(),
        "NAME": st.column_config.TextColumn(width="medium")
    }
)