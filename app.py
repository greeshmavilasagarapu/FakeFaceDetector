import streamlit as st
from app import dashboard, deepfake_detection, face_detection, suspicious_activity_detection
from pages import Uploads, Analysis, Reports

# Page configuration
st.set_page_config(
    page_title="FakeFaceDetector",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("🧠 Fake Face Detector")
st.sidebar.markdown("Ensure authentic video interviews with AI-powered deepfake detection.")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Uploads", "Analysis", "Reports"]
)

# Render pages
if page == "Dashboard":
    dashboard.show()
elif page == "Uploads":
    Uploads.show()
elif page == "Analysis":
    Analysis.show()
elif page == "Reports":
    Reports.show()
else:
    st.error("Page not found.")
