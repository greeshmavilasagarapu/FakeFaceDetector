# app/dashboard.py
import streamlit as st
import tempfile
from pathlib import Path
import pandas as pd
import cv2
from app.deepfake_detection import predict_video_authenticity
from app.suspicious_activity_detection import analyze_video_for_activity
from app.face_detection import draw_faces

def show():
    st.title("🎬 Interview Authenticity Checker (Recorded Video)")
    st.markdown("Upload a pre-recorded interview or record one using your webcam for analysis.")

    # --- Upload or Record ---
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    cam_record = st.camera_input("Or record a short video clip")

    if uploaded_file:
        tmp_path = Path(tempfile.gettempdir()) / uploaded_file.name
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())
        video_path = tmp_path
    elif cam_record:
        video_path = Path(tempfile.gettempdir()) / "camera_recording.mp4"
        with open(video_path, "wb") as f:
            f.write(cam_record.getbuffer())
    else:
        st.info("Please upload or record a video to start.")
        return

    st.video(str(video_path))
    sample_rate = st.slider("Frame Sampling Rate", 1, 30, 8, help="Lower value → slower but more accurate")

    if st.button("🔍 Run Analysis"):
        with st.spinner("Analyzing video... please wait"):
            # Deepfake Analysis
            authenticity = predict_video_authenticity(video_path, sample_rate=sample_rate)
            st.progress(60)

            # Suspicious Activity
            activity = analyze_video_for_activity(video_path, sample_rate=sample_rate)
            st.progress(85)

            # Snapshot of faces
            snapshot_path = Path("outputs/snapshot_faces.jpg")
            draw_faces(video_path, snapshot_path)
            st.progress(100)

        # --- Results ---
        if authenticity > 80:
            color, verdict = "#16a34a", "✅ Likely Real"
        elif authenticity > 50:
            color, verdict = "#eab308", "⚠️ Check Carefully"
        else:
            color, verdict = "#dc2626", "❌ Likely Fake"

        st.markdown
