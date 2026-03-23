import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. SETUP TIME DATA FIRST ---
tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
hour = now.hour
minute = now.minute
current_time = now.strftime("%H:%M:%S")

# --- 2. DEBUGGER SECTION ---
st.sidebar.header("Developer Tools")
manual_mode = st.sidebar.checkbox("Manual Time Override")

if manual_mode:
    # Use the slider value
    decimal_time = st.sidebar.slider("Test Time", 0.0, 23.9, float(hour + minute/60))
    st.sidebar.warning(f"Viewing: {int(decimal_time):02d}:{int((decimal_time%1)*60):02d}")
else:
    # Use real time
    decimal_time = hour + (minute / 60)

# --- 3. LOGIC FOR OWL VS SUN ---
if decimal_time >= 17.0 or decimal_time < 6.5:
    status = "Sleepy Time"
    bg_color = "#0C1445" 
    text_color = "white"
    icon = "🦉" 
else:
    status = "Wake Up Time!"
    bg_color = "#FFD700" 
    text_color = "black"
    icon = "☀️"

# --- 4. PROGRESS LOGIC ---
show_progress = False
if 5.5 <= decimal_time <= 7.5:
    show_progress = True
    progress_val = (decimal_time - 5.5) / 2.0

# --- 5. STYLING & UI ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 2s;
    }}
    .big-text {{
        font-size: 80px !important;
        font-weight: bold;
        text-align: center;
    }}
    .time-text {{
        font-size: 40px;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<p class="big-text">{icon}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="big-text">{status}</p>', unsafe_allow_html=True)

# Show real time only if NOT in manual mode to avoid confusion
if not manual_mode:
    st.markdown(f'<p class="time-text">{current_time}</p>', unsafe_allow_html=True)

if show_progress:
    st.write("The sun is waking up...")
    st.progress(min(max(progress_val, 0.0), 1.0))

# --- 6. AUTO-REFRESH (Only in real-time mode) ---
if not manual_mode:
    time.sleep(10)
    st.rerun()
