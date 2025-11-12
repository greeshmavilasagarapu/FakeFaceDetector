# app/live_monitor.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoTransformerBase
import av
import cv2
import numpy as np

from app.face_detection import draw_faces
from app.deepfake_detection import predict_frame_authenticity  # you'll add this helper below

def show_live_monitor():
    st.title("🕵️ Live Interview Monitor")
    st.markdown("Monitor real-time interview authenticity via webcam feed.")

    class VideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.counter = 0

        def transform(self, frame: av.VideoFrame):
            img = frame.to_ndarray(format="bgr24")
            self.counter += 1

            if self.counter % 5 == 0:  # sample every 5th frame
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    score = predict_frame_authenticity(rgb)
                    label = f"Score: {score*100:.1f}% Real"
                    color = (0, 255, 0) if score > 0.7 else (0, 165, 255) if score > 0.5 else (0, 0, 255)
                except Exception:
                    label, color = "Processing...", (255, 255, 255)

                cv2.putText(img, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Draw faces overlay
            try:
                img = draw_faces(img)
            except:
                pass

            return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="interview",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=VideoProcessor,
        rtc_configuration={"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False}
    )

    st.info("✅ Allow camera access to start live monitoring.")
