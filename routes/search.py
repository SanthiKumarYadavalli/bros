import streamlit as st
import utils
import datetime

if not st.session_state.get("image_serial"):
    st.session_state.image_serial = 0


def render_results(bros_data):
    one_bro = bros_data.shape[0] == 1
    if not one_bro:
        bros_list = st.dataframe(
            bros_data[['IMG', 'ID', 'NAME', 'PHONE', 'BRANCH']], 
            width="stretch",
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
            column_config={"IMG": st.column_config.ImageColumn()}
        )
        st.caption(f"count: :green[{bros_data.shape[0]}]")
    
    # display a bro's full data
    # result is one bro or user selected a bro from the dataframe
    if one_bro or len(bros_list.selection.rows):
        bro_data = bros_data.iloc[0 if one_bro else bros_list.selection.rows[0]]
        col1, col2 = st.columns([0.93, 0.07], gap=None, vertical_alignment="center")
        with col1:
            st.subheader(bro_data['NAME'], width="content")
        with col2:
            if st.button("💜"):
                st.session_state.image_serial += 1
                st.rerun()
        col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
        bro_data.name = ""  # hide table header

        with col1:  # image col
            image, serial = utils.get_image(bro_data['ID'], st.session_state.image_serial)
            st.session_state.image_serial = serial
            st.image(image)

        with col2:  # details col
            cols = [
                'ID', 'GENDER', 'DOB', 'AGE', 'BRANCH', 'FATHER', 'MOTHER', 'CASTE',
                'MANDAL', 'DISTRICT', 'SCHOOL', 'PHONE', 'Parent',
                'BLOOD GROUP', 'SSC', 'ADDRESS', 'CGPA'
            ]
            display_df = bro_data[cols]
            display_df["DOB"] = display_df["DOB"].strftime("%d %B %Y")
            st.dataframe(display_df.dropna().astype(str), width="stretch")

        # BIRTHDAY BRO
        if bro_data['DOB'].month == today.month and bro_data['DOB'].day == today.day:
            st.balloons()

        if bro_data.notna()['PHONE']:
            st.link_button(
                ":green[Whatsapp]",
                f"https://wa.me/+91{bro_data.PHONE}",
                width="stretch"
            )
            st.link_button(
                ":blue[Call]",
                f"tel:{bro_data.PHONE}",
                width="stretch"
            )


def render_input_field(selected_field):
    datalist = data['DOB'].dt.strftime("%Y-%m-%d") if selected_field == 'DOB' else data[selected_field]
    return st.selectbox(
        selected_field, datalist.dropna().sort_values().unique(),
        placeholder=f"Enter {selected_field}", index=None
    )


data = utils.get_data()
today = datetime.date.today()
search_fields = ["NAME", "ID", "PHONE", "DOB", "BRANCH", "IMAGE",
                 'GENDER', "MANDAL", "DISTRICT", "CASTE", "SCHOOL", "FATHER", "MOTHER"]
selected_fields = st.multiselect("By", search_fields, default="NAME", 
                                 placeholder="Choose some options")
uploaded_image = False
if "IMAGE" in selected_fields:
    uploaded_image = True
    selected_fields.remove("IMAGE")
    
col1, col2 = st.columns(2)
nfields = len(selected_fields)
q, r = divmod(nfields, 2)
selected_map = {}
with col1:
    for i in range(0, nfields - r, 2):
        selected_map[selected_fields[i]] = render_input_field(selected_fields[i])

with col2:
    for i in range(1, nfields, 2):
        selected_map[selected_fields[i]] = render_input_field(selected_fields[i]) 
               
if r:
    selected_map[selected_fields[-1]] = render_input_field(selected_fields[-1])

if uploaded_image:
    uploaded_image = st.file_uploader("Upload an Image")

queries = []
for selected_field, selected_value in selected_map.items():
    if not selected_value:
        continue
    if selected_field == 'DOB':
        selected_value = datetime.datetime.strptime(selected_value, "%Y-%m-%d")
    queries.append(f"({selected_field} == '{selected_value}')")
query = "&".join(queries)

if query or uploaded_image:    
    bros_data = data
    if query:    
        bros_data = bros_data.query(query)
    if uploaded_image:
        bros_data = utils.get_bro_from_image(uploaded_image, bros_data)
    if type(bros_data) != int:
        bros_data = bros_data.reset_index()
        bros_data.index += 1
        render_results(bros_data)
    else:
        st.write("No face detected in the uploaded image.")
