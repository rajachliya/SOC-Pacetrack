import streamlit as st

st.set_page_config(
    page_title="Fitness Dashboard",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Dark theme using CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
    }
    [data-testid="stMetricValue"] {
        color: #f0f6fc !important;
    }
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
    }
    p, label {
        color: #8b949e !important;
    }
</style>
""", unsafe_allow_html=True)

#Sidebar
with st.sidebar:
    st.title("🏃 Fitness Dashboard")
    st.write("Track your runs, health, and progress.")
    st.divider()

    st.subheader("📂 Upload Your Data")
    uploaded_file = st.file_uploader(
        "Upload activity file",
        type=["csv", "gpx", "json"],
        help="Upload a CSV, GPX or JSON file"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
    else:
        st.info("No file uploaded yet.")

    st.divider()
    st.subheader("🗺️ Navigation")
    st.write("📊 Dashboard")
    st.write("🏅 Activities")
    st.write("❤️ Health")
    st.write("📈 Progress")

#  Main Page 
st.title("📊 My Fitness Dashboard")
st.write("Welcome! Upload a file from the sidebar to get started.")
st.divider()

#  3 Metric Cards 
st.subheader("Core Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🗺️ Total Distance",
        value="-- km"
    )

with col2:
    st.metric(
        label="⏱️ Average Pace",
        value="-- min/km"
    )

with col3:
    st.metric(
        label="❤️ Heart Rate",
        value="-- bpm"
    )

st.divider()

# Placeholder Chart 
st.subheader("📈 Distance This Week")
st.caption("Upload a file to see your real data here.")

import pandas as pd

placeholder = pd.DataFrame({
    "Distance (km)": [0, 0, 0, 0, 0, 0, 0]
}, index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

st.bar_chart(placeholder)

st.divider()

#  Two extra placeholder cards 
col4, col5 = st.columns(2)

with col4:
    st.subheader("🏅 Recent Activities")
    st.write("No activities yet. Upload a file to see your runs here.")

with col5:
    st.subheader("❤️ Heart Rate Zones")
    st.write("No heart rate data yet. Upload a file to see your zones here.")
