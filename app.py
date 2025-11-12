import streamlit as st
import sys
import os

# --- Path Setup to allow importing from 'core' folder ---
# This is the key fix for the ImportError!
current_dir = os.path.dirname(__file__)
core_dir = os.path.join(current_dir, "core")

# Add the 'core' directory to the Python path
if core_dir not in sys.path:
    sys.path.append(core_dir)
# --------------------------------------------------------

# Since dashboard.py is now in 'pages', we only need to import the page-specific functions
# from the 'pages' directory. However, we'll keep the navigation explicit for flexibility.

# Import the page modules from the 'pages' folder (assuming they are in the same directory as app.py)
# This will not work if the files are truly in a subfolder called 'pages' as per your structure.
# For simplicity and to match the rest of your original code, we will rely on sys.path hack for now:
pages_dir = os.path.join(current_dir, "pages")
if pages_dir not in sys.path:
    sys.path.append(pages_dir)
    
# Import Page Modules (now that 'pages' folder is on the path)
import dashboard  # dashboard.py is now in 'pages'
import Uploads
import Analysis
import reports

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
    reports.show()
else:
    st.error("Page not found.")
