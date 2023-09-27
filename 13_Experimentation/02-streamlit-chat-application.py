import os
import streamlit as st
from dotenv import load_dotenv
import openai

load_dotenv()


def initialize_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
        
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    prompt = st.chat_input("What is up?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        return True
    return False


def prepare_assistant_messages():
    return [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]


def generate_assistant_response(assistant_messages):
    print(assistant_messages)
    response = openai.ChatCompletion.create(
        model=st.session_state["openai_model"], messages=assistant_messages
    )
    return response.choices[0].message["content"]


def main():
    st.title("ChatGPT-like clone")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    initialize_session_state()
    display_messages()

    if handle_user_input():
        assistant_messages = prepare_assistant_messages()
        assistant_response = generate_assistant_response(assistant_messages)

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )


if __name__ == "__main__":
    main()
