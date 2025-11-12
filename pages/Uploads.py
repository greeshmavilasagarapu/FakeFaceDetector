import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Uploads", layout="wide")
st.title("Upload Your Video")

# File uploader
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

# Save file if uploaded
if uploaded_file:
    save_path = Path("app/uploads")  # ensure this folder exists
    save_path.mkdir(parents=True, exist_ok=True)
    file_location = save_path / uploaded_file.name
    with open(file_location, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Saved file: {uploaded_file.name}")
    st.video(str(file_location))
