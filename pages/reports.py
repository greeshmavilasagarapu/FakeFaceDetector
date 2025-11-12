import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Reports", layout="wide")
st.title("Analysis Reports")

# Assuming you store results in app/outputs/results.csv
results_file = Path("app/outputs/results.csv")

if results_file.exists():
    df = pd.read_csv(results_file)
    st.dataframe(df)
    st.download_button(
        label="Download Report",
        data=df.to_csv(index=False),
        file_name="fakeface_report.csv",
        mime="text/csv"
    )
else:
    st.warning("No reports found. Run Analysis first.")
