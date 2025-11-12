
"""
deepfake_detection.py
Light wrapper to run a frame-wise prediction using a Keras model
(or fall back to a DeepFace-based heuristic if model not provided).
This stub is ready to be replaced with a real DFDC/Xception model file.
"""

from pathlib import Path
from typing import Optional, List
import numpy as np
import cv2
import logging

try:
    from tensorflow.keras.models import load_model
except Exception:
    load_model = None  # model loading may not be available in test env

# Path where you will place the pretrained model (optional)
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "deepfake_model.h5"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepfake")


def _load_keras_model(model_path: Path):
    if load_model is None:
        raise RuntimeError("Keras not available in this environment.")
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    logger.info("Loading model from %s", model_path)
    return load_model(str(model_path))


def _frame_predict(model, frame: np.ndarray) -> float:
    """
    Expect model to return probability of 'fake' (between 0 and 1).
    Resize and normalize the frame as required by your model.
    """
    img = cv2.resize(frame, (224, 224))
    img = img.astype("float32") / 255.0
    # model expects batch dimension
    pred = model.predict(np.expand_dims(img, 0))
    # normalize different output shapes
    if pred.ndim == 2:
        pred_val = float(pred[0, 0])
    else:
        pred_val = float(np.squeeze(pred))
    return float(np.clip(pred_val, 0.0, 1.0))


def predict_video_authenticity(video_path: Path, model_path: Optional[Path] = None, sample_rate: int = 10) -> float:
    """
    Runs through the video and returns an 'authenticity' score (0-100).
    sample_rate: process every Nth frame to speed up the demo.
    """
    if model_path and model_path.exists():
        model = _load_keras_model(model_path)
    else:
        model = None
        logger.warning("No model provided — using simple heuristic (DeepFace fallback).")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    scores: List[float] = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % sample_rate != 0:
            continue
        try:
            if model is not None:
                fake_prob = _frame_predict(model, frame)
            else:
                # simple heuristic: check if face is detected and not empty
                from deepface import DeepFace  # local import for fallback
                # this may raise if no face; treat as suspicious
                analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                fake_prob = 0.1 if analysis else 0.5
        except Exception as e:
            logger.debug("Prediction error on frame %s: %s", frame_idx, e)
            fake_prob = 0.5
        scores.append(fake_prob)

    cap.release()
    if not scores:
        return 0.0
    mean_fake_prob = float(np.mean(scores))
    authenticity = max(0.0, 100.0 * (1.0 - mean_fake_prob))
    logger.info("Video authenticity score: %.2f%%", authenticity)
    return authenticity


if __name__ == "__main__":
    from pathlib import Path
    v = Path("data/sample_video.mp4")
    try:
        score = predict_video_authenticity(v, model_path=MODEL_PATH if MODEL_PATH.exists() else None, sample_rate=15)
        print("Authenticity:", f"{score:.2f}%")
    except Exception as err:
        print("deepfake_detection error:", err)
