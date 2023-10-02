import streamlit as st

# st.chat_input is how we instatiate the chat input widget.
prompt = st.chat_input("Type something")
# When you start the app, the chat input is at first none. this is why
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
