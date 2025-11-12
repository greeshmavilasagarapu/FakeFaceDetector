import streamlit as st
# Corrected Imports: Directly import from the 'core' folder (which is now on sys.path)
import deepfake_detection
import face_detection
import suspicious_activity_detection

def show():
    st.title("📝 Reports")

    uploaded_file = st.session_state.get("uploaded_file", None)
    if uploaded_file:
        st.write(f"Generating report for: **{uploaded_file.name}**")

        # Save the uploaded file to disk temporarily for processing by CV2/Path modules
        temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # You can generate a simple text report combining results
        deepfake_result = deepfake_detection.analyze(temp_file_path)
        face_result = face_detection.detect_faces(temp_file_path)
        suspicious_result = suspicious_activity_detection.analyze_video_for_activity(temp_file_path)

        st.subheader("Analysis Report")
        st.write(f"🤖 **Deepfake Detection:** `{deepfake_result}`")
        st.write(f"👁️ **Face Detection:** `{face_result}`")
        st.write(f"🕵️ **Suspicious Activity Detection:** `{suspicious_result}`")

        st.info("Report generated successfully. You can expand this to downloadable PDFs or CSVs.")
    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
