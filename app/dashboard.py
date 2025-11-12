import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Dashboard")
    st.write("Welcome! Track your video analysis and suspicious activities here.")

    # Example summary stats
    st.subheader("Summary")
    st.metric("Videos Analyzed", "12")
    st.metric("Deepfake Detected", "2")
    st.metric("Pending Analysis", "3")
    
    st.info("Use the sidebar to navigate to Uploads, Analysis, or Reports.")
