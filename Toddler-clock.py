import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import time

# --- 0. PAGE CONFIG ---
# Must be the first Streamlit command. Forces sidebar open by default.
st.set_page_config(
    page_title="Toddler Clock",
    initial_sidebar_state="expanded"
)

# --- 1. SIDEBAR / LOCATION SETTINGS ---
st.sidebar.header("🌍 Location Settings")

all_tz = pytz.all_timezones
# London first, Barcelona second as requested
favorites = ['Europe/London', 'Europe/Barcelona']
final_tz_list = favorites + [tz for tz in all_tz if tz not in favorites]

selected_tz = st.sidebar.selectbox(
    "Select your Timezone",
    options=final_tz_list,
    index=0  # Defaults to London
)

# --- 2. TIME SETUP ---
try:
    tz = pytz.timezone(selected_tz)
except Exception:
    tz = pytz.timezone('UTC')

now = datetime.now(tz)
hour = now.hour
minute = now.minute

st.sidebar.markdown("---")
st.sidebar.header("⏰ Schedule Settings")
sleep_start_i = st.sidebar.time_input("Sleep Time Starts", dt_time(19, 0))
wake_up_i = st.sidebar.time_input("Wake Time Starts", dt_time(7, 0))
show_clock = st.sidebar.checkbox("Show Digital Clock", value=True)

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Developer Tools")
manual_mode = st.sidebar.checkbox("Manual Time Override (Preview)")

# Determine time string (12-hour format, no leading zero, no am/pm)
if manual_mode:
    decimal_time = st.sidebar.slider("Test Time", 0.0, 23.9, float(hour + minute/60))
    h_24 = int(decimal_time)
    m = int((decimal_time % 1) * 60)
    h_12 = h_24 % 12
    h_12 = 12 if h_12 == 0 else h_12
    current_time_string = f"{h_12}.{m:02d}"
else:
    decimal_time = hour + (minute / 60)
    # %-I removes leading zero on Linux/Streamlit Cloud
    current_time_string = now.strftime("%-I.%M")

# --- 3. LOGIC & COLORS ---
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

# --- 4. CSS (Corrected Header Cleanup) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        font-family: 'Inter', sans-serif;
        transition: background 3s ease-in-out;
    }}

    /* 1. HIDE ONLY THE RIGHT-SIDE ICONS (Fork, GitHub, Deploy) */
    /* We leave the left side of the header alone so the button stays */
    [data-testid="stHeaderActionElements"], .stDeployButton {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* 2. THE PARENT CONTROLS BUTTON STYLE */
    /* We make it a floating circular button so it's easy to tap */
    [data-testid="stSidebarCollapseButton"] {{
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        color: white !important;
        z-index: 999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }}

    /* 3. MAIN CARD STYLING */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 60px 20px;
        text-align: center;
        max-width: 500px;
        margin: 60px auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    }}
    
    .icon-div {{ font-size: 100px; margin-bottom: 20px; animation: pulse 4s infinite ease-in-out; }}
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.05); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.9; }}
    }}
    
    .status-label {{ font-size: 42px; font-weight: 700; color: {text_color}; margin-bottom: 10px; }}
    .clock-label {{ font-size: 32px; color: {text_color}; opacity: 0.8; font-weight: 400; }}

    /* Keep the header background clear so it doesn't block the card */
    header {{ background: transparent !important; }}
    footer {{ visibility: hidden !important; }}
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

# --- 6. AUTO-REFRESH ---
if not manual_mode:
    time.sleep(5)
    st.rerun()
