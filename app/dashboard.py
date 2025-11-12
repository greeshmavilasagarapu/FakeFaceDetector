import streamlit as st
import tempfile
import time
from pathlib import Path
import cv2
import numpy as np

# --- Import your AI modules ---
from app.deepfake_detection import predict_video_authenticity, predict_frame_authenticity
from app.face_detection import draw_faces
from app.suspicious_activity_detection import analyze_video_for_activity

# --- Page Config ---
st.set_page_config(page_title="🕵️ Fake Face Detector Dashboard", layout="wide")

st.title("🕵️ Fake Face Detector Dashboard")
st.markdown("Upload a video or image to check authenticity, or run a live interview mode.")

# --- Mode Selection ---
mode = st.radio("Select Mode", ["Recorded Video", "Live Interview"], horizontal=True)

# --- RECORDED VIDEO MODE ---
if mode == "Recorded Video":
    uploaded_video = st.file_uploader(
        "Upload a video",
        type=["mp4", "avi", "mov", "mpeg4"],
        help="Limit 200MB per file"
    )
    uploaded_photo = st.file_uploader(
        "Upload reference photo (optional)",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_video:
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
            with st.spinner("Analyzing video..."):
                # --- Deepfake Detection ---
                try:
                    authenticity = predict_video_authenticity(video_path)
                    st.success(f"Authenticity Score: **{authenticity:.2f}%**")
                except Exception as e:
                    st.error(f"Deepfake analysis failed: {e}")

                # --- Suspicious Activity ---
                try:
                    activity_report = analyze_video_for_activity(video_path)
                    st.subheader("Suspicious Activity Report")
                    st.json(activity_report)
                except Exception as e:
                    st.warning(f"Activity detection failed: {e}")

                # --- Face Detection Snapshot ---
                try:
                    snapshot_path = str(Path(tempfile.gettempdir()) / "faces_snapshot.jpg")
                    draw_faces(video_path, snapshot_path)
                    st.image(snapshot_path, caption="Detected Faces Snapshot")
                except Exception as e:
                    st.warning(f"Face snapshot failed: {e}")

# --- LIVE INTERVIEW MODE ---
else:
    st.subheader("🎙️ Live Interview Mode")
    st.markdown("This mode activates your webcam and performs real-time monitoring.")

    start_button = st.button("Start Live Interview")
    stop_button = st.button("Stop Live Interview")

    if start_button:
        stframe = st.empty()
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Unable to access webcam. Check your permissions.")
        else:
            st.info("Press 'Stop Live Interview' button or refresh page to end session.")

            live_scores = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # --- Deepfake Frame Score ---
                try:
                    score = predict_frame_authenticity(frame_rgb)
                except Exception:
                    score = 0  # fallback
                live_scores.append(score)

                # --- Overlay score on frame ---
                cv2.putText(
                    frame_rgb,
                    f"Authenticity: {score*100:.2f}%",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0) if score > 0.5 else (255, 0, 0),
                    2,
                    cv2.LINE_AA
                )

                stframe.image(frame_rgb, channels="RGB", use_container_width=True)

                time.sleep(0.1)

                if stop_button:
                    break

            cap.release()
            if live_scores:
                avg_score = np.mean(live_scores) * 100
                st.success(f"Session Authenticity Score: **{avg_score:.2f}%**")

st.markdown("---")
st.markdown("**Note:** This is a prototype. Replace the simulated deepfake model with a real CNN/DeepFace model for production use.")
