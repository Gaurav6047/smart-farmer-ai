import streamlit as st
import time

def fancy_loader(text="Processing..."):
    with st.spinner(text):
        time.sleep(0.6)

    # Fake progress bar for smooth visual experience
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)
