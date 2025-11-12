import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Uploads")
    st.write("Upload a video or image to start analysis.")

    uploaded_file = st.file_uploader(
        "Drag and drop a file here",
        type=["mp4", "jpg", "png", "jpeg", "mpeg4"],
        help="Limit 200MB per file"
    )

    if uploaded_file:
        st.success(f"Uploaded {uploaded_file.name} successfully!")
        st.info("Now go to Analysis page to run detection.")
