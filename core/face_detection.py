# app/face_detection.py
from pathlib import Path
import cv2

def detect_faces_in_image(image_path: Path):
    """
    Detect faces in an image and return dummy bounding boxes.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return []
    h, w = img.shape[:2]
    # Return one rectangle in the center for demo
    return [(w//4, h//4, w//2, h//2)]

def draw_faces(video_path: Path, output_path: Path):
    """
    Draw a dummy rectangle on the first frame of the video as snapshot.
    """
    cap = cv2.VideoCapture(str(video_path))
    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise FileNotFoundError(f"Cannot read video: {video_path}")

    h, w = frame.shape[:2]
    cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 3)
    cv2.imwrite(str(output_path), frame)
    cap.release()
