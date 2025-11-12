import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Reports")
    st.write("View analysis results and reports of your uploads here.")

    st.info("No analysis available yet." if st.session_state.get("analysis_done") is None else "")
    
    # Example placeholder table
    st.subheader("Analysis Summary")
    st.table({
        "File": ["video1.mp4", "image1.jpg"],
        "Deepfake Detected": ["No", "Yes"],
        "Suspicious Activity": ["No", "Yes"]
    })
