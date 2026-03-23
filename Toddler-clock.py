import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import time

# --- 1. SETUP & TIMEZONE ---
tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
curr_s = now.hour + (now.minute / 60)

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Settings")
sleep_start_i = st.sidebar.time_input("Sleep Time", dt_time(19, 0)) # Default 7pm
wake_up_i = st.sidebar.time_input("Wake Time", dt_time(7, 0))     # Default 7am
show_clock = st.sidebar.checkbox("Show Digital Clock", value=True)

# --- 3. LOGIC & TRANSPOSED THEME ---
sleep_s = sleep_start_i.hour + (sleep_start_i.minute / 60)
wake_s = wake_up_i.hour + (wake_up_i.minute / 60)

if curr_s >= sleep_s or curr_s < wake_s:
    # Night Palette (Indigo/Slate from Lovable)
    status, icon = "Sleepy Time", "🌙"
    bg_gradient = "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)"
    card_bg = "rgba(30, 27, 75, 0.4)"
    accent_color = "#818cf8" # Indigo 400
    text_color = "#e0e7ff"
else:
    # Day Palette (Amber/Yellow from Lovable)
    status, icon = "Rise & Shine!", "☀️"
    bg_gradient = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"
    card_bg = "rgba(255, 255, 255, 0.6)"
    accent_color = "#d97706" # Amber 600
    text_color = "#78350f"

# --- 4. CSS TRANSPOSED FROM LOVABLE (Tailwind-like styles) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        font-family: 'Inter', sans-serif;
        transition: background 3s ease-in-out;
    }}
    
    /* The Glass Card */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 60px 20px;
        text-align: center;
        max-width: 500px;
        margin: 80px auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    }}
    
    /* Animated Icon */
    .icon-div {{
        font-size: 100px;
        margin-bottom: 20px;
        animation: pulse 4s infinite ease-in-out;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.1); opacity: 1; }}
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
        font-size: 20px;
        font-weight: 400;
        color: {text_color};
        opacity: 0.7;
    }}

    /* Hide Streamlit elements for a cleaner UI */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
st.markdown(f"""
    <div class="glass-card">
        <div class="icon-div">{icon}</div>
        <div class="status-label">{status}</div>
        {"<div class='clock-label'>" + now.strftime("%H:%M") + "</div>" if show_clock else ""}
    </div>
    """, unsafe_allow_html=True)

# Progress Bar (Last 2 hours of sleep)
if (wake_s - 2.0) <= curr_s < wake_s:
    cols = st.columns([1, 4, 1])
    with cols[1]:
        progress = (curr_s - (wake_s - 2.0)) / 2.0
        st.progress(min(max(progress, 0.0), 1.0))
        st.markdown(f"<p style='text-align:center; color:{text_color}; font-size:14px;'>Morning is almost here...</p>", unsafe_allow_html=True)

# --- 6. LIVE REFRESH ---
time.sleep(5)
st.rerun()
