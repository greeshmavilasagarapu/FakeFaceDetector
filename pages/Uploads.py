import streamlit as st
import tempfile
import os

def show():
    st.title("📤 Upload File")
    
    # Ensure uploaded_file key exists in session state
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
        
    uploaded_file = st.file_uploader(
        "Drag and drop a file here (e.g., MP4, JPEG)",
        type=["mp4", "jpg", "png", "jpeg", "mpeg4"],
        accept_multiple_files=False
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.session_state["uploaded_file"] = uploaded_file
    elif st.session_state["uploaded_file"]:
        st.info(f"Currently loaded: {st.session_state['uploaded_file'].name}")
    else:
        st.warning("Please upload a file to begin analysis.")
