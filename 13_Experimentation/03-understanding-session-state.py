import streamlit as st

st.title("Streamlit Session Stat")

# session state can either be a dictionary or the attributes of an objects

# This is how we initialize it something inside of the session state.
if 'messages' not in st.session_state:
    st.session_state.messages = ["hello, world!"]
    # OR
    st.session_state['counter'] = 0

st.session_state
st.write(st.session_state.counter)
st.write(st.session_state.messages)

# We can access all the keys by:
for key in st.session_state.keys():
    st.write(key)


for value in st.session_state.values():
    st.write(value)

# All items
for item in st.session_state.items():
    st.write(item)

button = st.button("update state")

"before pressing button:", st.session_state.counter

if button:
    st.session_state.counter += 1
    "after pressing button",    st.session_state.counter

# How to clear session_state
for key in st.session_state.keys():
    del st.session_state[key]

# Once again, its an empty list.
st.session_state
