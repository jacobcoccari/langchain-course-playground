import streamlit as st
import numpy as np

# When you use user, ai, assistant, or human, streamlit will automatically assign a thumbnail to it.
human_message = st.chat_message("user")
human_message.write("Hello 👋")

ai_message = st.chat_message("ai")
ai_message.write("Hello human")
ai_message.bar_chart(np.random.randn(30, 3))
