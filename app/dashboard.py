# app/dashboard.py
import sys
from pathlib import Path
import streamlit as st

# Add app folder to path so Python can find modules
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

from deepfake_detection import predict_video_authenticity, MODEL_PATH
from face_detection import detect_faces_in_image, draw_faces
from suspicious_activity_detection import analyze_video_for_activity

# --- Folders ---
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# --- Default files ---
default_video = next(DATA_DIR.glob("*.mp4"), None)
default_photo = next(DATA_DIR.glob("*.jpg"), None)

# --- Streamlit Config ---
st.set_page_config(page_title="Interview Authenticity", layout="wide")
st.title("Interview Authenticity Checker — Prototype")

# --- Instructions ---
st.write("""
Upload a short interview video and optionally an ID photo.
Click **Run Analysis** to see results.
If no upload is made, default sample files from `data/` will be used.
""")

# --- File Upload ---
uploaded_video = st.file_uploader("Upload interview video", type=["mp4", "mov", "avi"])
uploaded_photo = st.file_uploader("Upload ID photo (optional)", type=["jpg", "png", "jpeg"])

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

# --- Previews ---
if video_path and video_path.exists():
    st.video(str(video_path))
if photo_path and photo_path.exists():
    st.image(str(photo_path), caption="ID Photo / Reference Image", width=300)

# --- Run Analysis ---
if st.button("Run Analysis"):
    if not video_path or not video_path.exists():
        st.error("❌ No video available. Upload one or place it in the data folder.")
    else:
        # Deepfake score
        st.info("Running deepfake analysis...")
        try:
            authenticity = predict_video_authenticity(video_path, model_path=MODEL_PATH if MODEL_PATH.exists() else None)
            st.success(f"Authenticity score: {authenticity:.2f}%")
        except Exception as e:
            st.warning(f"Could not run deepfake analysis: {e}")

        # Suspicious activity
        st.info("Checking suspicious activity...")
        try:
            activity_report = analyze_video_for_activity(video_path)
            st.json(activity_report)
        except Exception as e:
            st.warning(f"Could not run activity analysis: {e}")

        # Face snapshot
        try:
            snapshot_path = OUT_DIR / "snapshot_faces.jpg"
            draw_faces(video_path, snapshot_path)
            st.image(str(snapshot_path), caption="Detected faces snapshot")
        except Exception as e:
            st.warning(f"Could not create face snapshot: {e}")

# Notes
st.markdown("""
**Notes:**  
- Demo prototype.  
- Replace models with real deepfake and activity detection models for production.
""")
