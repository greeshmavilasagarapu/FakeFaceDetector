
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import time

# Ensure app/ modules are importable
BASE_DIR = Path(__file__).resolve().parents[1]   # repo root
sys.path.append(str(BASE_DIR / "app"))

from deepfake_detection import predict_video_authenticity, MODEL_PATH
from face_detection import draw_faces
from suspicious_activity_detection import analyze_video_for_activity

# Folders
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# Defaults
default_video = next(DATA_DIR.glob("*.mp4"), None)
default_photo = next(DATA_DIR.glob("*.jpg"), None)

st.set_page_config(page_title="Dashboard — Interview Authenticity Checker", layout="wide")

# Styling
st.markdown("""
<style>
.stApp { background-color: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
.header { background-color: #1f2937; color: white; padding: 1rem 2rem; border-radius: 5px; margin-bottom: 1rem; }
[data-testid="stSidebar"] { background-color: #e5e7eb; padding: 1rem; }
.stButton>button {
    background-color: #2563eb !important;
    color: white !important;
    font-size: 16px !important;
    height: 45px !important;
    border-radius: 6px !important;
    border: none !important;
}
.card { background-color: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 20px; margin-top: 20px; }
.card-header { background-color: #2563eb; color: white; padding: 10px 15px; border-radius: 8px 8px 0 0; font-weight: bold; font-size: 18px; }
.card-content { padding: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h2>Interview Authenticity Checker</h2></div>', unsafe_allow_html=True)

# Sidebar: Uploads & settings
st.sidebar.title("Upload & Settings")
uploaded_video = st.sidebar.file_uploader("Upload Interview Video", type=["mp4","mov","avi"])
uploaded_photo = st.sidebar.file_uploader("Upload ID Photo (optional)", type=["jpg","png","jpeg"])
sample_rate = st.sidebar.slider("Frame Sample Rate", min_value=1, max_value=30, value=8)
st.sidebar.markdown("---")
st.sidebar.markdown("If no files are uploaded, default files from `data/` will be used.")

# Choose files
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

# Tabs layout
tab1, tab2, tab3 = st.tabs(["Upload", "Analysis Results", "Face Snapshots"])

with tab1:
    st.subheader("Video Preview")
    if video_path and video_path.exists():
        st.video(str(video_path))
    else:
        st.info("Upload a video to preview here.")
    st.subheader("Reference Photo")
    if photo_path and photo_path.exists():
        st.image(str(photo_path), width=300)
    else:
        st.info("Upload a reference photo to preview here.")

with tab2:
    run = st.button("Run Analysis", use_container_width=True)
    if run:
        if not video_path or not video_path.exists():
            st.error("No video available. Upload one or place it in the data/ folder.")
        else:
            authenticity = None
            activity_report = {}

            # Deepfake: spinner
            with st.spinner("Analyzing video authenticity..."):
                time.sleep(0.5)
                try:
                    authenticity = predict_video_authenticity(video_path, model_path=MODEL_PATH if MODEL_PATH.exists() else None, sample_rate=sample_rate)
                except Exception as e:
                    st.warning(f"Deepfake analysis failed: {e}")
                    authenticity = None

            # Display deepfake card
            if authenticity is not None:
                if authenticity > 80:
                    color, status = "#16a34a", "Likely Real"
                elif authenticity > 50:
                    color, status = "#eab308", "Check Carefully"
                else:
                    color, status = "#dc2626", "Likely Fake"

                st.markdown(f"""<div style="background:{color};color:white;padding:18px;border-radius:8px;text-align:center;font-weight:600;">Deepfake Score: {authenticity:.2f}% — {status}</div>""", unsafe_allow_html=True)

            # Suspicious activity
            with st.spinner("Checking suspicious activity..."):
                time.sleep(0.4)
                try:
                    activity_report = analyze_video_for_activity(video_path, sample_rate=sample_rate)
                except Exception as e:
                    st.warning(f"Activity analysis failed: {e}")
                    activity_report = {}

            st.markdown('<div class="card-header">Suspicious Activity Report</div>', unsafe_allow_html=True)
            st.markdown('<div class="card card-content">', unsafe_allow_html=True)
            if activity_report:
                st.table(pd.DataFrame([activity_report]))
            else:
                st.info("No activity data available.")
            st.markdown("</div>", unsafe_allow_html=True)

            # Summary card
            with st.spinner("Compiling summary..."):
                time.sleep(0.3)
                st.markdown('<div class="card-header">Summary Report</div>', unsafe_allow_html=True)
                st.markdown('<div class="card card-content">', unsafe_allow_html=True)

                total_frames = activity_report.get("frames_processed", 0)
                multi_face = activity_report.get("multiple_face_events", 0)
                no_face = activity_report.get("no_face_events", 0)

                col1, col2, col3 = st.columns(3)
                if authenticity is not None:
                    col1.metric("Authenticity Score", f"{authenticity:.2f}%")
                col2.metric("Frames Processed", total_frames)
                col3.metric("Multiple Faces", multi_face)
                st.markdown("---")

                if authenticity is not None:
                    if authenticity < 60:
                        st.warning("The video may be inauthentic. Review manually.")
                    elif multi_face > 5:
                        st.warning("Multiple faces detected — possible tampering or background interference.")
                    else:
                        st.success("The video appears authentic and consistent.")
                st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.subheader("Detected Faces Snapshot")
    with st.spinner("Generating snapshot..."):
        try:
            snapshot_path = OUT_DIR / "snapshot_faces.jpg"
            draw_faces(video_path, snapshot_path)
            st.image(str(snapshot_path))
        except Exception:
            st.info("Snapshot will appear here after analysis.")
