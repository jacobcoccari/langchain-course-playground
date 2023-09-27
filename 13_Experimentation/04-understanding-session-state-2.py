import streamlit as st

st.title("Session State Part II")

"Starting session state object:", st.session_state

# This works with all widgets
# We can GET the state from the widget like this.
# Say we had a slider.
number = st.slider("A number", 1, 100, key="slider")

st.write(st.session_state.slider)

"-----------------------------------------------"

# Let's say we wanted to use a item in your state to update a widget.

# Now, we can set up some custom logic that updates session state based on the widget value.
next_button = st.button("Next")

if next_button:
    if st.session_state.radio_option == 'Comedy':
        st.session_state.radio_option = 'Drama'
    elif st.session_state.radio_option == 'Drama':
        st.session_state.radio_option = 'Documentary'
    else:
        st.session_state.radio_option = 'Comedy'

genre = st.radio(
    "What's your favorite movie genre",
    ["Comedy", "Drama", "Documentary"],
    key="radio_option"
)
st.session_state

if genre == 'Comedy':
    st.write('You selected comedy.')
elif genre == 'Drama':
    st.write('You selected drama.')
else:
    st.write('You selected documentary.')
