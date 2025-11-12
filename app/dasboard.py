# fakefacedetector/app/dashboard.py
import streamlit as st

st.set_page_config(page_title="Fake Face Detector", layout="wide")

st.title("🕵️ Fake Face Detector Dashboard")

uploaded_file = st.file_uploader("Upload a video or image", type=["mp4", "jpg", "png"])
if uploaded_file is not None:
    st.video(uploaded_file) if uploaded_file.name.endswith(".mp4") else st.image(uploaded_file)
    st.write("✅ File uploaded successfully! (Model analysis coming soon...)")
else:
    st.info("Please upload a file to begin analysis.")
