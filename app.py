import streamlit as st
from app import dashboard
from pages import Uploads, Analysis, Reports  # new pages

# Page configuration
st.set_page_config(
    page_title="FakeFaceDetector",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("🧠 Fake Face Detector")
st.sidebar.markdown("Ensure authentic video interviews with AI-powered deepfake detection.")

# Add all pages to the sidebar
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
    st.error("Page not found. Please select from the sidebar.")
