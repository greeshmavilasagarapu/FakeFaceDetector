# app/dashboard.py
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import time

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
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #1d4ed8 !important;
}
.card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 20px;
    margin-top: 20px;
}
.card-header {
    background-color: #2563eb;
    color: white;
    padding: 10px 15px;
    border-radius: 8px 8px 0 0;
    font-weight: bold;
    font-size: 18px;
}
.card-content {
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header"><h2>Interview Authenticity Checker</h2></div>', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Upload & Settings")
uploaded_video = st.sidebar.file_uploader("Upload Interview Video", type=["mp4", "mov", "avi"])
uploaded_photo = st.sidebar.file_uploader("Upload ID Photo (optional)", type=["jpg", "png", "jpeg"])
sample_rate = st.sidebar.slider("Frame Sample Rate", min_value=1, max_value=30, value=8)
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

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📤 Upload", "📊 Analysis Results", "🖼️ Face Snapshots"])

# --- Tab 1: Upload ---
with tab1:
    st.subheader("Video Preview")
    if video_path and video_path.exists():
        st.video(str(video_path))
    else:
        st.info("Upload a video to preview it here.")

    st.subheader("ID / Reference Photo")
    if photo_path and photo_path.exists():
        st.image(str(photo_path), width=300)
    else:
        st.info("Upload a reference photo to preview it here.")

# --- Tab 2: Analysis Results ---
with tab2:
    run_button = st.button("Run Analysis 🚀", use_container_width=True)

    if run_button:
        if not video_path or not video_path.exists():
            st.error("No video available. Upload one or place it in the data folder.")
        else:
            # --- Deepfake Analysis ---
            with st.spinner("Analyzing video authenticity... Please wait."):
                time.sleep(1)
                try:
                    authenticity = predict_video_authenticity(
                        video_path,
                        model_path=MODEL_PATH if MODEL_PATH.exists() else None,
                        sample_rate=sample_rate
                    )
                except Exception as e:
                    authenticity = None
                    st.warning(f"Could not run deepfake analysis: {e}")

            if authenticity is not None:
                if authenticity > 80:
                    color, status = "#16a34a", "Likely Real"
                elif authenticity > 50:
                    color, status = "#eab308", "Check Carefully"
                else:
                    color, status = "#dc2626", "Likely Fake"

                st.markdown(f"""
                <div style="
                    background-color:{color};
                    color:white;
                    padding:20px;
                    border-radius:10px;
                    text-align:center;
                    font-size:22px;
                    font-weight:bold;">
                    Deepfake Score: {authenticity:.2f}% — {status}
                </div>
                """, unsafe_allow_html=True)

            # --- Suspicious Activity ---
            with st.spinner("Checking for suspicious activities..."):
                time.sleep(1)
                try:
                    activity_report = analyze_video_for_activity(video_path, sample_rate=sample_rate)
                    st.markdown('<div class="card-header">Suspicious Activity Report</div>', unsafe_allow_html=True)
                    st.markdown('<div class="card card-content">', unsafe_allow_html=True)
                    report_df = pd.DataFrame([activity_report])
                    st.table(report_df)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Could not run activity analysis: {e}")

            # --- Summary Report ---
            with st.spinner("Compiling summary..."):
                time.sleep(0.8)
                try:
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
                            st.warning("⚠️ The video may be *inauthentic*. Please verify manually.")
                        elif multi_face > 5:
                            st.warning("⚠️ Multiple faces detected — possible tampering or background interference.")
                        else:
                            st.success("✅ The video appears authentic and visually consistent.")
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.info(f"Could not generate summary: {e}")

# --- Tab 3: Faces ---
with tab3:
    st.subheader("Detected Faces Snapshot")
    with st.spinner("Generating face snapshot..."):
        try:
            snapshot_path = OUT_DIR / "snapshot_faces.jpg"
            draw_faces(video_path, snapshot_path)
            st.image(str(snapshot_path))
        except Exception:
            st.info("Face snapshot will appear here after analysis.")

# --- Footer ---
st.markdown("""
---
**Notes:**  
- Demo prototype for portfolio use.  
- Replace placeholder models with production-level ML systems.  
- Streamlined with fast execution and responsive feedback.
""")

