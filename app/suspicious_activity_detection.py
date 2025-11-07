# app/suspicious_activity_detection.py
"""
Suspicious activity detection stub for demo purposes.
Uses OpenCV Haar cascade to count:
 - frames with no face
 - frames with multiple faces
Returns a simple dictionary report.
"""

from pathlib import Path
import cv2
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("activity")

# Haar cascade for face detection
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def analyze_video_for_activity(video_path: Path, sample_rate: int = 5) -> Dict[str, int]:
    """
    Analyze video for simple suspicious activity heuristics.
    Returns a dictionary report.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    frames_processed = 0
    multiple_face_events = 0
    no_face_events = 0
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % sample_rate != 0:
            continue
        frames_processed += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            no_face_events += 1
        elif len(faces) > 1:
            multiple_face_events += 1

    cap.release()

    # Create a simple report dictionary
    report = {
        "frames_processed": frames_processed,
        "multiple_face_events": multiple_face_events,
        "no_face_events": no_face_events,
        "notes": "Demo analysis — replace with real activity tracker for production."
    }

    logger.info("Activity report: %s", report)
    return report


# --- Test run ---
if __name__ == "__main__":
    sample_video = Path("data/sample_video.mp4")
    if sample_video.exists():
        result = analyze_video_for_activity(sample_video)
        print("Activity report:", result)
    else:
        print("No sample video found in data/")
