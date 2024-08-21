import streamlit as st
import face_recognition
import utils

data = utils.get_data()

img = st.camera_input("Let's see who you are")
if img:
    img = face_recognition.load_image_file(img)
    enc = face_recognition.face_encodings(img)
    if enc:
        distances = data['enc'].dropna().apply(lambda e: face_recognition.face_distance([e], enc[0])[0])
        mindex = distances.idxmin()
        st.write(f"I'm {100 - round(distances[mindex] * 100, 2)}% sure that")
        st.header(f"You're :blue[{data.loc[distances.idxmin(), 'NAME'].title()}]")
        