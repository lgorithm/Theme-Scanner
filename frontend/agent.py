import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import requests

load_dotenv()
host = os.getenv('HOST')

st.header("ThemeScanner Agent 📑")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def onSend():
    with st.spinner("Generating response.."):
        prompt = st.session_state.user_input
        
        generated_response = requests.post(
            url=f"{host}/send/",
            json={"query": prompt}
        )
        if generated_response.status_code == 200:
            generated_response = generated_response.json()
        print('response:', generated_response)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(generated_response["answer"])
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))
        
chat_placeholder = st.empty()

with chat_placeholder.container():     
    if st.session_state["chat_answers_history"]:
        i=0
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(user_query, is_user=True, key=f"user_{i}")
            message(generated_response, key=f"bot_{i}")
            i+=1
        
with st.container():
    st.chat_input(on_submit=onSend, placeholder="Enter your prompt here..", key="user_input")