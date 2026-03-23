import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import time

# --- 0. PREVENT SIDEBAR FROM HIDING ---
# This MUST be the first streamlit command
st.set_page_config(
    page_title="Toddler Clock",
    initial_sidebar_state="expanded" 
)

# --- 1. SETUP & TIMEZONE ---
tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
hour = now.hour
minute = now.minute

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ App Settings")
sleep_start_i = st.sidebar.time_input("Sleep Time Starts", dt_time(19, 0))
wake_up_i = st.sidebar.time_input("Wake Time Starts", dt_time(7, 0))
show_clock = st.sidebar.checkbox("Show Digital Clock", value=True)

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Developer Tools")
manual_mode = st.sidebar.checkbox("Manual Time Override (Preview)")

if manual_mode:
    decimal_time = st.sidebar.slider("Test Time of Day", 0.0, 23.9, float(hour + minute/60))
    display_hour = int(decimal_time)
    display_min = int((decimal_time % 1) * 60)
    current_time_string = f"{display_hour:02d}:{display_min:02d}"
else:
    decimal_time = hour + (minute / 60)
    current_time_string = now.strftime("%H:%M")

# --- 3. LOGIC ---
sleep_s = sleep_start_i.hour + (sleep_start_i.minute / 60)
wake_s = wake_up_i.hour + (wake_up_i.minute / 60)

if decimal_time >= sleep_s or decimal_time < wake_s:
    status, icon = "Sleepy Time", "🌙"
    bg_gradient = "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)"
    card_bg = "rgba(30, 27, 75, 0.4)"
    text_color = "#e0e7ff"
else:
    status, icon = "Rise & Shine!", "☀️"
    bg_gradient = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"
    card_bg = "rgba(255, 255, 255, 0.6)"
    text_color = "#78350f"

# --- 4. CSS ---
# --- 4. CSS (Corrected to show the sidebar button) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        font-family: 'Inter', sans-serif;
        transition: background 3s ease-in-out;
    }}

    /* --- SIDEBAR BUTTON FIX --- */
    /* This ensures the ">" arrow is visible and clickable */
    [data-testid="stSidebarCollapseButton"] {{
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 50%;
        color: white !important;
        z-index: 999999;
        display: block !important;
    }}
    
    /* Hover effect for the button */
    [data-testid="stSidebarCollapseButton"]:hover {{
        background-color: rgba(255, 255, 255, 0.4) !important;
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 60px 20px;
        text-align: center;
        max-width: 500px;
        margin: 40px auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    }}
    
    .icon-div {{
        font-size: 100px;
        margin-bottom: 20px;
        animation: pulse 4s infinite ease-in-out;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.05); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.9; }}
    }}
    
    .status-label {{
        font-size: 42px;
        font-weight: 700;
        color: {text_color};
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }}
    
    .clock-label {{
        font-size: 24px;
        color: {text_color};
        opacity: 0.8;
    }}

    /* Hide the rest of the junk but keep the app functional */
    footer {{visibility: hidden;}}
    header {{background-color: transparent !important;}}
    </style>
    """, unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown(f"""
    <div class="glass-card">
        <div class="icon-div">{icon}</div>
        <div class="status-label">{status}</div>
        {"<div class='clock-label'>" + current_time_string + "</div>" if show_clock else ""}
    </div>
    """, unsafe_allow_html=True)

# Progress Bar (Last 2 hours before wake-up)
if (wake_s - 2.0) <= decimal_time < wake_s:
    cols = st.columns([1, 4, 1])
    with cols[1]:
        progress = (decimal_time - (wake_s - 2.0)) / 2.0
        st.progress(min(max(progress, 0.0), 1.0))
        st.markdown(f"<p style='text-align:center; color:{text_color}; font-size:14px; opacity:0.8;'>Morning is almost here...</p>", unsafe_allow_html=True)

# --- 6. LIVE REFRESH ---
if not manual_mode:
    time.sleep(5)
    st.rerun()
