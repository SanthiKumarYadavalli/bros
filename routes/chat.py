import streamlit as st
from gemini.agent import initialize_chat, send_message
import time
import random

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Hey! 😄 I know all the R20 student stuff —  got questions or need some charts? Let’s go! 📊✨"
        }
    )

if 'chat' not in st.session_state:
    try:
        st.session_state.chat = initialize_chat()
    except Exception as e:
        if "429" in str(e):
            st.error("Error initializing chat: Rate limit exceeded. Need money 💵")
        else:
            st.error(f"Error initializing chat: {e}")
        st.stop()


st.title("Let's chat!")

# --- Display Chat History ---
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("chart"):
            st.plotly_chart(message["chart"], use_container_width=True)

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


    if st.session_state.messages[-1]["role"] == "assistant":  # If the last message was from the assistant, update it
        st.session_state.messages[-1]["content"] = full_response
    else:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()  # Rerun to update the chart display
