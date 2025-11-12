import streamlit as st
from app import dashboard, login, about

# Sidebar navigation
st.sidebar.title("🧠 Fake Face Detector")
page = st.sidebar.radio("Navigate", ["Login", "Dashboard", "About"])

if page == "Login":
    login.show()
elif page == "Dashboard":
    dashboard.show()
else:
    about.show()
