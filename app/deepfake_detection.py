# app/deepfake_detection.py
"""
Deepfake Detection Module
-------------------------
Handles AI-based deepfake analysis for both recorded and live video frames.

Functions:
- predict_video_authenticity(video_path, sample_rate=8): analyzes a full video.
- predict_frame_authenticity(frame_rgb): analyzes a single frame (for live feed).

This module currently uses simulated deepfake detection scores for demonstration.
In a production version, replace simulated logic with a pre-trained CNN or transformer-based model.
"""

import cv2
import numpy as np
import random
from pathlib import Path

# Optional: path to pretrained model (if available)
MODEL_PATH = Path("models/deepfake_model.pth")


def predict_video_authenticity(video_path, sample_rate=8, model_path=None):
    """
    Predict the authenticity score of a video by sampling frames.

    Args:
        video_path (str | Path): Path to the video file.
        sample_rate (int): Analyze every nth frame to save time.
        model_path (str | Path, optional): Path to trained model.

    Returns:
        float: Authenticity percentage (0–100), higher means more likely real.
    """
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    scores = []
    frame_count = 0

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % sample_rate == 0:
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Simulated deepfake detection — replace with actual model later
            frame_score = _simulate_model_prediction(rgb_frame)
            scores.append(frame_score)

        frame_count += 1

    cap.release()

    if len(scores) == 0:
        return 0.0

    avg_score = sum(scores) / len(scores)
    authenticity_percentage = float(avg_score * 100)
    return authenticity_percentage


def predict_frame_authenticity(frame_rgb):
    """
    Predict authenticity for a single frame (used in live interview monitoring).

    Args:
        frame_rgb (np.ndarray): RGB frame from webcam feed.

    Returns:
        float: Probability (0–1) that frame is real.
    """
    if frame_rgb is None or not isinstance(frame_rgb, np.ndarray):
        raise ValueError("Invalid frame input for deepfake detection.")

    # Simulated frame-level authenticity score
    return _simulate_model_prediction(frame_rgb)


def _simulate_model_prediction(frame_rgb):
    """
    Simulates deepfake model prediction logic.
    Replace this with your CNN/DeepFace/Transformer inference in production.
    """
    # Example logic: random variation simulating model confidence
    base_confidence = random.uniform(0.6, 0.99)

    # Add some frame brightness/noise factors to simulate variability
    brightness = np.mean(frame_rgb) / 255.0
    adjustment = (brightness - 0.5) * 0.1  # small brightness effect

    simulated_score = np.clip(base_confidence + adjustment, 0.0, 1.0)
    return simulated_score
