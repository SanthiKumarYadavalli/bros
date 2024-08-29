import streamlit as st
import utils
import datetime

data = utils.get_data()
today = datetime.date.today()

search_fields = ["ID", "NAME", "PHONE", "GENDER", 
                 "DOB", 'BRANCH', "MANDAL", "DISTRICT", "CASTE", "SCHOOL"]
selected_field = st.selectbox("By", search_fields)
datalist = data['DOB'].dt.strftime("%Y-%m-%d") if selected_field == 'DOB' else data[selected_field]
selected_value = st.selectbox(
    "Search", datalist.dropna().sort_values().unique(),
    placeholder=f"Enter {selected_field}", index=None
)

# fetching data
if selected_value:
    selected_value = datetime.datetime.strptime(selected_value, "%Y-%m-%d") if selected_field == 'DOB' \
                                                                          else selected_value
    bros_data = data.loc[data[selected_field] == selected_value].reset_index(drop=True)
    bros_data.index += 1
    bro_data = bros_data.iloc[0]
    if bros_data.shape[0] != 1:
        st.dataframe(bros_data[['ID', 'NAME', 'PHONE', 'BRANCH']], use_container_width=True)
    else:
        # DISPLAYING DATA  
        st.subheader(bro_data['NAME'], divider="rainbow")
        col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
        bro_data.name = ""  # hide table header

        with col1:  # image col
            st.image(utils.get_image(bro_data['ID']))

        with col2:  # details col
            cols = [
                'ID', 'GENDER', 'DOB', 'AGE', 'BRANCH', 'FATHER', 'MOTHER', 'CASTE',
                'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE', 'Parent',
                'BLOOD GROUP', 'ADDRESS', 'CGPA']
            display_df = bro_data[cols]
            display_df["DOB"] = display_df["DOB"].strftime("%d %B %Y")
            st.dataframe(display_df.dropna().astype(str), use_container_width=True)

        # BIRTHDAY BRO
        if bro_data['DOB'].month == today.month and bro_data['DOB'].day == today.day:
            st.balloons()

        if bro_data.notna()['PHONE']:
            st.link_button(
                ":green[Whatsapp]",
                f"https://wa.me/+91{bro_data.PHONE}",
                use_container_width=True
            )
            st.link_button(
                ":blue[Call]",
                f"tel:{bro_data.PHONE}",
                use_container_width=True
            )
