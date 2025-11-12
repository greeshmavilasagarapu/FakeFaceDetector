# app/dashboard.py
import sys
from pathlib import Path
import streamlit as st
import cv2
import tempfile
import time
import numpy as np

# Add app folder to path so Python can find modules
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

from deepfake_detection import predict_video_authenticity, predict_frame_authenticity, MODEL_PATH
from face_detection import detect_faces_in_image, draw_faces
from suspicious_activity_detection import analyze_video_for_activity

# --- Streamlit Config ---
st.set_page_config(page_title="Interview Authenticity Checker", layout="wide")

st.title("🎥 Interview Authenticity Checker — AI Powered")

st.write("""
This dashboard allows you to **verify authenticity** of digital interviews in two modes:
1. **Recorded Video Mode** — upload a pre-recorded video.  
2. **Live Interview Mode** — record and analyze in real-time using your webcam.
""")

# --- Mode Selection ---
mode = st.radio("Select Mode", ["Recorded Video", "Live Interview"], horizontal=True)

# --- Recorded Video Mode ---
if mode == "Recorded Video":
    uploaded_video = st.file_uploader("Upload interview video", type=["mp4", "mov", "avi"])
    uploaded_photo = st.file_uploader("Upload ID photo (optional)", type=["jpg", "png", "jpeg"])

    if uploaded_video:
        # Save uploaded video temporarily
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(uploaded_video.read())
        video_path = temp_video.name
        st.video(video_path)
    else:
        st.info("Please upload a video to begin analysis.")
        video_path = None

    if uploaded_photo:
        temp_photo = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_photo.write(uploaded_photo.read())
        photo_path = temp_photo.name
        st.image(photo_path, caption="Reference Photo", width=250)
    else:
        photo_path = None

    if st.button("Run Analysis"):
        if not video_path:
            st.error("Please upload a video first.")
        else:
            with st.spinner("Analyzing video... please wait."):
                try:
                    authenticity = predict_video_authenticity(video_path)
                    st.success(f"Authenticity Score: **{authenticity:.2f}%**")
                except Exception as e:
                    st.error(f"Deepfake analysis failed: {e}")

                try:
                    activity = analyze_video_for_activity(video_path)
                    st.subheader("Suspicious Activity Report")
                    st.json(activity)
                except Exception as e:
                    st.warning(f"Activity detection failed: {e}")

                try:
                    snapshot = str(Path(tempfile.gettempdir()) / "faces_snapshot.jpg")
                    draw_faces(video_path, snapshot)
                    st.image(snapshot, caption="Detected Faces Snapshot")
                except Exception as e:
                    st.warning(f"Face snapshot failed: {e}")

# --- Live Interview Mode ---
else:
    st.subheader("🎙️ Live Interview Mode")

    st.write("This mode activates your **webcam** and performs real-time face and deepfake monitoring.")

    start_button = st.button("Start Live Interview")

    if start_button:
        stframe = st.empty()
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Unable to access webcam. Please check your permissions.")
        else:
            st.info("Press 'Stop' in the toolbar or refresh the page to exit live mode.")

            frame_count = 0
            live_scores = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Get deepfake authenticity for this frame
                score = predict_frame_authenticity(frame_rgb)
                live_scores.append(score)

                # Show live feed with score
                cv2.putText(
                    frame_rgb,
                    f"Authenticity: {score * 100:.2f}%",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0) if score > 0.5 else (255, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

                stframe.image(frame_rgb, channels="RGB", use_container_width=True)

                frame_count += 1
                time.sleep(0.1)

            cap.release()
            avg_score = np.mean(live_scores) * 100
            st.success(f"Session Authenticity Score: **{avg_score:.2f}%**")

st.markdown("---")
st.markdown("**Note:** This is a prototype. Replace simulated deepfake model with a real trained CNN or DeepFace detector for production use.")
