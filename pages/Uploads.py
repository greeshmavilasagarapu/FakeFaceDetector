import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Uploads")
    st.write("Upload a video or image to start analysis.")

    uploaded_file = st.file_uploader(
        "Drag and drop a file here",
        type=["mp4", "jpg", "png", "jpeg", "mpeg4"],
        key="uploaded_file"
    )

    if uploaded_file:
        # Store the uploaded file in session state so other pages can access it
        st.session_state["uploaded_file"] = uploaded_file
        st.success(f"File uploaded: {uploaded_file.name}")

        # Preview the file
        if uploaded_file.type.startswith("video"):
            st.video(uploaded_file)
        else:
            st.image(uploaded_file)
    else:
        st.info("Please upload a file to begin analysis.")
