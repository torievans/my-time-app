import streamlit as st
from datetime import datetime
import pytz
import time

# 1. Setup Timezone (Change to your local zone, e.g., 'Europe/London')
tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
current_time = now.strftime("%H:%M:%S")
hour = now.hour
minute = now.minute
decimal_time = hour + (minute / 60)

# 2. Logic for Owl vs Sun
# Owl: 17:00 (5 PM) to 06:30 AM
if decimal_time >= 17.0 or decimal_time < 6.5:
    status = "Sleepy Time"
    bg_color = "#0C1445" # Deep night blue
    text_color = "white"
    icon = "🦉" 
else:
    status = "Wake Up Time!"
    bg_color = "#FFD700" # Sunny Gold
    text_color = "black"
    icon = "☀️"

# 3. Progress Logic (5:30 AM to 7:30 AM)
show_progress = False
if 5.5 <= decimal_time <= 7.5:
    show_progress = True
    # Calculate progress percentage (0.0 to 1.0)
    # 5.5 is start, 7.5 is end. Total duration = 2 hours.
    progress_val = (decimal_time - 5.5) / 2.0

# 4. Inject Styling
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

# 5. Display UI
st.markdown(f'<p class="big-text">{icon}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="big-text">{status}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="time-text">{current_time}</p>', unsafe_allow_html=True)

if show_progress:
    st.write("The sun is waking up...")
    st.progress(progress_val)

# 6. Auto-refresh every 30 seconds
time.sleep(30)
st.rerun()
# 5. Optional: Auto-refresh every minute
# time.sleep(60)
# st.rerun()
