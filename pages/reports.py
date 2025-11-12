import streamlit as st
# NEEDED FIX: Import os and tempfile for file handling
import os
import tempfile 
# Assuming 'core' folder structure and path setup in app.py:
import deepfake_detection
import face_detection
import suspicious_activity_detection

def show():
    st.title("📝 Reports")

    uploaded_file = st.session_state.get("uploaded_file", None)
    
    if uploaded_file:
        st.write(f"Generating report for: **{uploaded_file.name}**")

        # --- FIX: Save file object to a temporary disk path ---
        temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # ----------------------------------------------------

        # Pass the file path, NOT the uploaded file object, to your core modules
        deepfake_result = deepfake_detection.analyze(temp_file_path)
        face_result = face_detection.detect_faces(temp_file_path)
        suspicious_result = suspicious_activity_detection.detect_activity(temp_file_path)

        st.subheader("Analysis Report")
        st.write(f"🤖 **Deepfake Detection:** `{deepfake_result}`")
        st.write(f"👁️ **Face Detection:** `{face_result}`")
        st.write(f"🕵️ **Suspicious Activity Detection:** `{suspicious_result}`")

        st.info("Report generated successfully.")
        
        # Good practice: Clean up the temporary file
        os.remove(temp_file_path) 
    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
