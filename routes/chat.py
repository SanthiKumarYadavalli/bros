import streamlit as st
from gemini.agent import initialize_chat, send_message
import time
import random

st.title("Let's chat!") 

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": "Hey there!"}
    )

if 'chat' not in st.session_state:
    st.session_state.chat = initialize_chat()

# --- Display Chat History ---
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        full_response = ""
        message_placeholder.markdown("<p style='color: lightgreen'>Thinking...</p>", unsafe_allow_html=True)

        for chunk in send_message(st.session_state.chat, prompt).split(' '):
            full_response += chunk + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(random.uniform(0.05, 0.2))  # Simulate typing delay
        message_placeholder.markdown(full_response)


    st.session_state.messages.append({"role": "assistant", "content": full_response})
