import cv2
from pathlib import Path

def draw_faces(video_path):
    """
    Dummy face detection function.
    Returns the first frame with rectangles around faces.
    """
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None

    # Dummy rectangle (replace with actual face detection)
    height, width, _ = frame.shape
    cv2.rectangle(frame, (width//4, height//4), (width//2, height//2), (0,255,0), 2)

    # Convert BGR to RGB for Streamlit
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
