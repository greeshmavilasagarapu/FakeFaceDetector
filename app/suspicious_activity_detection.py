def analyze_video_for_activity(video_path):
    """
    Dummy suspicious activity detection.
    Replace with actual analysis logic.
    Saves results to app/outputs/results.csv
    """
    activity_detected = "No Suspicious Activity"

    # Save/append to results.csv
    from pathlib import Path
    import pandas as pd

    outputs_dir = Path("app/outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    results_file = outputs_dir / "results.csv"

    if results_file.exists():
        df = pd.read_csv(results_file)
    else:
        df = pd.DataFrame(columns=["Video", "Suspicious_Activity"])

    video_name = Path(video_path).name
    new_row = {"Video": video_name, "Suspicious_Activity": activity_detected}

    # Avoid duplicate rows for the same video by overwriting
    df = df[df.Video != video_name]
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(results_file, index=False)

    return activity_detected
