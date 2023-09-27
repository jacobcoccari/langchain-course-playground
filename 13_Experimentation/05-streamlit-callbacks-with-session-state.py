import streamlit as st

st.title("Streamlit Session State with Callbacks")

# on_change works for "input" widgets like sliders and number inputs
# on_click works for "one off" widgets like buttons and form submit buttons

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs / 2.2046
def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg * 2.2046

col1, buff, col2 = st.columns([2,1,2])

with col1:
    pounds = st.number_input("Enter a weight in pounds", key="lbs", on_change=lbs_to_kg,)

with col2:
    kilograms = st.number_input("Enter a weight in kilograms", key="kg", on_change=kg_to_lbs)

st.session_state