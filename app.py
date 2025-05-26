import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Bitcoin Price",
    page_icon="₿",  # Optional: Bitcoin emoji/icon
    layout="centered"  # or "wide"
)
st.title("Bitcoin Price Viewer")
st.markdown("Displays live and saved Bitcoin prices.")

DATA_FOLDER = "data"

def get_latest_snapshot():
    try:
        files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
        if not files:
            return None
        files.sort(reverse=True)
        latest_file = os.path.join(DATA_FOLDER, files[0])
        with open(latest_file) as f:
            data = json.load(f)
        return data, files[0]
    except Exception as e:
        st.error(f"Error loading snapshot: {e}")
        return None

snapshot = get_latest_snapshot()
if snapshot:
    data, filename = snapshot
    st.success(f"Latest snapshot file: {filename}")
    st.metric(label="Bitcoin Price (USD)", value=f"${data['bitcoin']['usd']}")
    st.caption(f"Snapshot taken at: {data['snapshot_time']}")
else:
    st.warning("No snapshot data found. Run your save_snapshot.py script first.")

if snapshot:
    with st.expander("View other snapshots"):
        files = sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")], reverse=True)
        selected_file = st.selectbox("Choose a snapshot", files)
        if selected_file:
            with open(os.path.join(DATA_FOLDER, selected_file)) as f:
                file_data = json.load(f)
            st.write(file_data)
