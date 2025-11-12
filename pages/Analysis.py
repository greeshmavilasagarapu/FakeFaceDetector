import streamlit as st
# Corrected Imports: Directly import from the 'core' folder (which is now on sys.path)
import deepfake_detection
import face_detection
import suspicious_activity_detection

def show():
    st.title("📊 Analysis")

    # Access the uploaded file from session state
    uploaded_file = st.session_state.get("uploaded_file", None)
    
    if uploaded_file:
        st.write(f"Analyzing file: **{uploaded_file.name}**")

        # Save the uploaded file to disk temporarily for processing by CV2/Path modules
        # This is crucial for your deepfake and face detection logic to work with CV2.
        temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("### Deepfake Detection")
        st.info(deepfake_detection.analyze(temp_file_path))

        st.write("### Face Detection")
        # In a real app, you'd show the frame, but for now, we'll just show the function result
        st.info(face_detection.detect_faces(temp_file_path))

        st.write("### Suspicious Activity Detection")
        st.info(suspicious_activity_detection.analyze_video_for_activity(temp_file_path))

    else:
        st.warning("No file uploaded yet. Please upload a file first in the Uploads page.")
