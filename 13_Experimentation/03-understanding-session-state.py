import streamlit as st

st.title("Streamlit Session Stat")

# session state can either be a dictionary or the attributes of an objects

if 'messages' not in st.session_state:
    st.session_state.messages = ["hello, world!"]

st.session_state

