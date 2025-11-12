import streamlit as st
from app.deepfake_detection import predict_video_authenticity
from app.face_detection import draw_faces
from app.suspicious_activity_detection import analyze_video_for_activity
from pathlib import Path

st.set_page_config(page_title="Analysis", layout="wide")
st.title("Video Analysis")

# List uploaded videos
upload_dir = Path("app/uploads")
videos = list(upload_dir.glob("*")) if upload_dir.exists() else []

if not videos:
    st.warning("No uploaded videos found. Please upload a video first on the Uploads page.")
else:
    video_choice = st.selectbox("Select a video to analyze", [v.name for v in videos])
    if video_choice:
        video_path = upload_dir / video_choice
        st.video(str(video_path))

        st.subheader("Face Detection")
        faces_img = draw_faces(str(video_path))
        st.image(faces_img, caption="Detected Faces", use_column_width=True)

        st.subheader("Deepfake Detection")
        result = predict_video_authenticity(str(video_path))
        st.write(f"Deepfake Analysis Result: **{result}**")

        st.subheader("Suspicious Activity Detection")
        activity = analyze_video_for_activity(str(video_path))
        st.write(f"Suspicious Activity Result: **{activity}**")
