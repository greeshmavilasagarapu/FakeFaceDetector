import streamlit as st
# NEEDED FIX: Import os and tempfile
import os
import tempfile
# Assuming 'core' folder structure and path setup in app.py:
import deepfake_detection
import face_detection
import suspicious_activity_detection

def show():
    st.title("📊 Analysis")

    uploaded_file = st.session_state.get("uploaded_file", None)
    
    if uploaded_file:
        st.write(f"Analyzing file: **{uploaded_file.name}**")

        # --- FIX: Temp file saving logic (Crucial for CV2) ---
        # The uploaded file object must be saved to a physical path for your CV2/Path modules to read it.
        # This is where the NameError was occurring because os/tempfile were missing.
        temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # ----------------------------------------------------

        st.write("### Deepfake Detection")
        # Pass the file path, NOT the uploaded file object, to your core modules
        st.info(deepfake_detection.analyze(temp_file_path)) 

        st.write("### Face Detection")
        st.info(face_detection.detect_faces(temp_file_path))

        st.write("### Suspicious Activity Detection")
        st.info(suspicious_activity_detection.detect_activity(temp_file_path))

        # OPTIONAL: Clean up the temp file after use (good practice)
        os.remove(temp_file_path)
    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
