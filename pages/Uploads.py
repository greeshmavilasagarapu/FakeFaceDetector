import streamlit as st

def show():
    st.title("📤 Upload File")
    uploaded_file = st.file_uploader(
        "Drag and drop a file here",
        type=["mp4", "jpg", "png", "jpeg", "mpeg4"],
        accept_multiple_files=False
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.session_state["uploaded_file"] = uploaded_file
