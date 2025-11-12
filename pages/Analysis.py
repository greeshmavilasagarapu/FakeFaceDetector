import streamlit as st
from app import deepfake_detection, face_detection, suspicious_activity_detection

def show():
    st.title("📊 Analysis")

    uploaded_file = st.session_state.get("uploaded_file", None)
    if uploaded_file:
        st.write(f"Analyzing file: {uploaded_file.name}")

        st.write("### Deepfake Detection")
        st.info(deepfake_detection.analyze(uploaded_file))

        st.write("### Face Detection")
        st.info(face_detection.detect_faces(uploaded_file))

        st.write("### Suspicious Activity Detection")
        st.info(suspicious_activity_detection.detect_activity(uploaded_file))

    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
