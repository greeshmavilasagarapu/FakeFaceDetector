# app/data_collection.py
"""
Utility to inspect / list files in the data folder
and provide a minimal summary.
"""

from pathlib import Path
from typing import List

# Default data folder
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def list_data_files(data_path: Path = DATA_DIR) -> List[Path]:
    """
    Return a list of all files (no recursion) in the data folder.
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_path}")
    return [p for p in data_path.iterdir() if p.is_file()]


def summary(data_path: Path = DATA_DIR) -> None:
    """
    Print a summary of files in the data folder, grouped by extension.
    """
    files = list_data_files(data_path)
    print(f"Data folder: {data_path}")
    if not files:
        print("  (no files found)")
        return

    counts = {}
    for f in files:
        counts[f.suffix.lower()] = counts.get(f.suffix.lower(), 0) + 1

    for ext, cnt in counts.items():
        print(f"  {ext}: {cnt} file(s)")
    print(f"  Total files: {len(files)}")


# --- Test run ---
if __name__ == "__main__":
    try:
        summary()
    except Exception as e:
        print("Error:", e)
