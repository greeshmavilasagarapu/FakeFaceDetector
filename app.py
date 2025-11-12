# app.py
import streamlit as st

st.set_page_config(page_title="Interview Authenticity App", layout="wide")

st.title("Interview Authenticity Checker — Home")
st.write("""
This app validates interview videos for deepfakes and suspicious activity.
Use the sidebar to navigate, or choose a page below.
""")

st.markdown("## Quick links")
st.markdown("- Go to **Dashboard** via the left pages menu.")
st.markdown("- View **Reports** and exported outputs.")
st.markdown("- Read **About** for tech stack and credits.")
