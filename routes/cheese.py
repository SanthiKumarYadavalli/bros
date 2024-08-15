import streamlit as st
import face_recognition
import utils

data = utils.get_data()

img = st.camera_input("Cheese!")
if img:
    st.image(img)
    img = face_recognition.load_image_file(img)
    enc = face_recognition.face_encodings(img)
    if enc:
        distances = data['enc'].dropna().apply(lambda e: face_recognition.face_distance([e], enc[0]))
        st.header(data.loc[distances.idxmin(), "NAME"])