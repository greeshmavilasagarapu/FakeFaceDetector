import streamlit as st
from app import deepfake_detection, face_detection, suspicious_activity_detection

def show():
    st.title("📝 Reports")

    uploaded_file = st.session_state.get("uploaded_file", None)
    if uploaded_file:
        st.write(f"Generating report for: {uploaded_file.name}")

        # You can generate a simple text report combining results
        deepfake_result = deepfake_detection.analyze(uploaded_file)
        face_result = face_detection.detect_faces(uploaded_file)
        suspicious_result = suspicious_activity_detection.detect_activity(uploaded_file)

        st.subheader("Analysis Report")
        st.write(f"🤖 Deepfake Detection: {deepfake_result}")
        st.write(f"👁️ Face Detection: {face_result}")
        st.write(f"🕵️ Suspicious Activity Detection: {suspicious_result}")

        st.info("Report generated successfully. You can expand this to downloadable PDFs or CSVs.")
    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
