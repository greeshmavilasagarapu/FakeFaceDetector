# core/data_collection.py
"""
Utility to inspect / list files in the data folder
and provide a minimal summary.
"""
from pathlib import Path
from typing import List

# Default data folder (This path might need adjustment depending on where you store data)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def list_data_files(data_path: Path = DATA_DIR) -> List[Path]:
    """
    Return a list of all files (no recursion) in the data folder.
    """
    if not data_path.exists():
        # In a real app, you might create the directory or point to a known location
        # raise FileNotFoundError(f"Data directory not found: {data_path}")
        return [] # Return empty list if data folder doesn't exist
    return [p for p in data_path.iterdir() if p.is_file()]

def summary(data_path: Path = DATA_DIR) -> str:
    """
    Return a summary string of files in the data folder.
    """
    try:
        files = list_data_files(data_path)
    except FileNotFoundError:
        return "Data directory not accessible."

    output = [f"Data folder: {data_path}"]
    if not files:
        output.append("  (no files found)")
        return "\n".join(output)

    counts = {}
    for f in files:
        counts[f.suffix.lower()] = counts.get(f.suffix.lower(), 0) + 1

    for ext, cnt in counts.items():
        output.append(f"  {ext}: {cnt} file(s)")
    output.append(f"  Total files: {len(files)}")
    
    return "\n".join(output)
