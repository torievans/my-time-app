import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import time

# --- 1. SETUP TIME DATA ---
tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
current_time_string = now.strftime("%H:%M:%S")

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("⏰ Schedule Settings")

# Set the default start/end times
sleep_start_input = st.sidebar.time_input("Sleepy Time Starts", dt_time(17, 0)) # Default 5:00 PM
wake_up_input = st.sidebar.time_input("Wake Up Time Starts", dt_time(7, 30))    # Default 7:30 AM

# Convert inputs to decimals for our logic (e.g., 7:30 -> 7.5)
sleep_start = sleep_start_input.hour + (sleep_start_input.minute / 60)
wake_up_start = wake_up_input.hour + (wake_up_input.minute / 60)

# --- 3. DEBUGGER SECTION ---
st.sidebar.header("🛠️ Developer Tools")
manual_mode = st.sidebar.checkbox("Manual Time Override")

if manual_mode:
    decimal_time = st.sidebar.slider("Test Time", 0.0, 23.9, float(now.hour + now.minute/60))
    st.sidebar.warning(f"Viewing: {int(decimal_time):02d}:{int((decimal_time%1)*60):02d}")
else:
    decimal_time = now.hour + (now.minute / 60)

# --- 4. UPDATED LOGIC ---
# The "Night" condition: If time is AFTER sleep starts OR BEFORE wake up starts
if decimal_time >= sleep_start or decimal_time < wake_up_start:
    status = "Sleepy Time"
    bg_color = "#0C1445" 
    text_color = "white"
    icon = "🦉" 
else:
    status = "Wake Up Time!"
    bg_color = "#FFD700" 
    text_color = "black"
    icon = "☀️"

# --- 5. PROGRESS LOGIC (Starts 2 hours before wake up) ---
show_progress = False
progress_window_start = wake_up_start - 2.0

if progress_window_start <= decimal_time < wake_up_start:
    show_progress = True
    # Calculate progress over that 2-hour window
    progress_val = (decimal_time - progress_window_start) / 2.0
    progress_val = min(max(progress_val, 0.0), 1.0)

# --- 6. STYLING & UI ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 2s;
    }}
    .big-text {{
        font-size: 100px !important;
        text-align: center;
        margin-bottom: 0px;
    }}
    .status-text {{
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: -30px;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<p class="big-text">{icon}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="status-text">{status}</p>', unsafe_allow_html=True)

if not manual_mode:
    st.markdown(f'<div style="text-align:center; opacity:0.6;">{current_time_string}</div>', unsafe_allow_html=True)

if show_progress:
    st.write("---")
    st.write("The sun is waking up...")
    st.progress(progress_val)

# --- 7. AUTO-REFRESH ---
if not manual_mode:
    time.sleep(10)
    st.rerun()
