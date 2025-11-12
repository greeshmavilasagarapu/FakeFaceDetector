import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Dashboard")
    st.write("Welcome! Track your video analysis and suspicious activities here.")

    # Example summary stats
    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Videos Analyzed", "12")
    col2.metric("Deepfake Detected", "2")
    col3.metric("Pending Analysis", "3")
    
    st.info("Use the sidebar to navigate to Uploads, Analysis, or Reports.")
