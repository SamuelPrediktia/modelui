import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Prediktia's predictive model! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
   For the magic to start select Analyze prediction tab
"""
)
