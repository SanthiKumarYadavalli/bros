import streamlit as st
import face_recognition
import utils

qmap = {
    "Everyone": "Everyone",
    "OpGender": "Opposite Gender",
    "Celebs": "Celebrities"
}

vs = st.selectbox("bros to compare with", qmap.values())

if vs != qmap["Celebs"]:
    data = utils.get_data()[['enc', "GENDER", "NAME", "ID"]]
    data.rename(columns={"enc": "ENCODINGS"}, inplace=True)
    data.dropna(subset=["ENCODINGS"], inplace=True)
else:
    data = utils.get_famous_bros()


img = st.camera_input("Take a photo")

if img:
    img = face_recognition.load_image_file(img)
    enc = face_recognition.face_encodings(img)
    if enc:    
        data['DISTANCE'] = data["ENCODINGS"].apply(lambda e: face_recognition.face_distance([e], enc[0])[0])
        mindex = data["DISTANCE"].idxmin()
        predicted_bro = data.loc[mindex]
        if vs == qmap["OpGender"]:
            brogender = predicted_bro['GENDER']
            data = data[data["GENDER"] == ("MALE" if brogender == "FEMALE" else "FEMALE")]
            mindex = data["DISTANCE"].idxmin()
            predicted_bro = data.loc[mindex]
        
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.write(f"I'm {100 - round(predicted_bro['DISTANCE'] * 100, 2)}% sure that")
            st.header(f"You're{' looking like ' if vs != qmap['Everyone'] else ' '}:blue[{predicted_bro['NAME'].title()}]")
        with col2:
            if vs != qmap["Celebs"]:
                st.image(utils.get_image(predicted_bro['ID']))
            else:
                st.link_button("Who?", f"https://www.google.com/search?q={predicted_bro['NAME']}")
    else:
        st.write("No face detected.")