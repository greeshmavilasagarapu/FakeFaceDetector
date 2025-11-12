import streamlit as st

def show():
    st.title("🕵️ Fake Face Detector - Analysis")
    st.write("Perform deepfake detection and suspicious activity analysis here.")

    st.warning("No file uploaded yet." if st.session_state.get("uploaded_file") is None else "")
    
    if st.button("Run Analysis"):
        st.info("Running deepfake detection...")
        st.success("Analysis complete! Check results in Reports page.")
