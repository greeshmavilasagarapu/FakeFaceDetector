import cv2
import pandas as pd
from pathlib import Path

def predict_video_authenticity(video_path):
    """
    Dummy deepfake prediction function.
    Replace with your actual model inference.
    Saves results to app/outputs/results.csv
    """
    # Example prediction logic (replace with your model)
    fake_score = 0.3  # e.g., 0.3 means real-ish
    result = "Fake" if fake_score > 0.5 else "Real"

    # Save to outputs
    outputs_dir = Path("app/outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    results_file = outputs_dir / "results.csv"

    # Append to CSV or create new
    if results_file.exists():
        df = pd.read_csv(results_file)
    else:
        df = pd.DataFrame(columns=["Video", "Deepfake_Result", "Fake_Score"])

    video_name = Path(video_path).name
    new_row = {"Video": video_name, "Deepfake_Result": result, "Fake_Score": fake_score}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(results_file, index=False)

    return result
