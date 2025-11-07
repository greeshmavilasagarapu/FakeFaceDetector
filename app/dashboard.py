# app/dashboard.py
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add app folder to path so Python can find modules
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

from deepfake_detection import predict_video_authenticity, MODEL_PATH
from face_detection import draw_faces
from suspicious_activity_detection import analyze_video_for_activity

# --- Folders ---
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# --- Default files ---
default_video = next(DATA_DIR.glob("*.mp4"), None)
default_photo = next(DATA_DIR.glob("*.jpg"), None)

# --- Streamlit Config ---
st.set_page_config(
    page_title="Interview Authenticity Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #f8f9fa;
}

/* Top bar styling */
.header {
    background-color: #1f2937;
    color: white;
    padding: 1rem 2rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #e5e7eb;
    padding: 1rem;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    font-size: 16px;
    height: 45px;
    border-radius: 5px;
}

/* Tables */
.stTable {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --- Top Navigation / Header ---
st.markdown('<div class="header"><h2>Interview Authenticity Checker</h2></div>', unsafe_allow_html=True)

# Optional: add logo on top right
st.markdown("""
<div style="text-align:right; margin-bottom:10px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Logo_of_Streamlit.svg/1200px-Logo_of_Streamlit.svg.png" width="100">
</div>
""", unsafe_allow_html=True)

# --- Sidebar for Uploads & Settings ---
st.sidebar.title("Upload & Settings")
uploaded_video = st.sidebar.file_uploader("Upload Interview Video", type=["mp4", "mov", "avi"])
uploaded_photo = st.sidebar.file_uploader("Upload ID Photo (optional)", type=["jpg", "png", "jpeg"])
sample_rate = st.sidebar.slider("Frame Sample Rate", min_value=1, max_value=30, value=8, help="Lower = more frames processed, slower but more accurate")

st.sidebar.markdown("---")
st.sidebar.markdown("If no files are uploaded, default files from `data/` will be used.")

# --- Decide which files to use ---
if uploaded_video:
    video_path = DATA_DIR / uploaded_video.name
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
elif default_video:
    video_path = default_video
else:
    video_path = None

if uploaded_photo:
    photo_path = DATA_DIR / uploaded_photo.name
    with open(photo_path, "wb") as f:
        f.write(uploaded_photo.read())
elif default_photo:
    photo_path = default_photo
else:
    photo_path = None

# --- Main Content Layout with Columns ---
col1, col2 = st.columns(2)

with col1:
    if video_path and video_path.exists():
        st.subheader("Video Preview")
        st.video(str(video_path))
    if photo_path and photo_path.exists():
        st.subheader("ID / Reference Photo")
        st.image(str(photo_path), width=300)

with col2:
    if st.button("Run Analysis"):
        if not video_path or not video_path.exists():
            st.error("No video available. Upload one or place it in the data folder.")
        else:
            # Deepfake Score
            st.subheader("Deepfake Analysis")
            try:
                authenticity = predict_video_authenticity(video_path, model_path=MODEL_PATH if MODEL_PATH.exists() else None, sample_rate=sample_rate)
                if authenticity > 80:
                    st.success(f"Authenticity Score: {authenticity:.2f}% — Likely Real")
                elif authenticity > 50:
                    st.warning(f"Authenticity Score: {authenticity:.2f}% — Check Carefully")
                else:
                    st.error(f"Authenticity Score: {authenticity:.2f}% — Likely Fake")
            except Exception as e:
                st.warning(f"Could not run deepfake analysis: {e}")

            # Suspicious Activity
            st.subheader("Suspicious Activity Report")
            try:
                activity_report = analyze_video_for_activity(video_path, sample_rate=sample_rate)
                report_df = pd.DataFrame([activity_report])
                st.table(report_df)
            except Exception as e:
                st.warning(f"Could not run activity analysis: {e}")

            # Face Snapshot
            st.subheader("Detected Faces Snapshot")
            try:
                snapshot_path = OUT_DIR / "snapshot_faces.jpg"
                draw_faces(video_path, snapshot_path)
                st.image(str(snapshot_path))
            except Exception as e:
                st.warning(f"Could not create face snapshot: {e}")

# --- Footer Notes ---
st.markdown("""
---
**Notes:**  
- Demo prototype for portfolio purposes.  
- Replace placeholder models with production-level models for deployment.
""")
