
import streamlit as st
from pathlib import Path
import pandas as pd

st.title("Reports")
OUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
st.write("Generated outputs (snapshots, CSVs)")

if OUT_DIR.exists():
    files = list(OUT_DIR.iterdir())
    if not files:
        st.info("No outputs yet. Run an analysis to generate snapshots/reports.")
    else:
        file = st.selectbox("Select file", files)
        if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            st.image(str(file))
        elif file.suffix.lower() in [".csv", ".json"]:
            try:
                df = pd.read_csv(file) if file.suffix.lower() == ".csv" else pd.read_json(file)
                st.dataframe(df)
            except Exception as e:
                st.write("Cannot preview this file:", e)
else:
    st.warning("Outputs folder not found.")
