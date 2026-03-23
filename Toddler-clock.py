import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import time

# --- 0. PAGE CONFIG ---
st.set_page_config(
    page_title="Toddler Clock",
    initial_sidebar_state="expanded"
)

# --- 1. SIDEBAR / LOCATION ---
st.sidebar.header("🌍 Location Settings")
all_tz = pytz.all_timezones
favorites = ['Europe/London', 'Europe/Barcelona']
final_tz_list = favorites + [tz for tz in all_tz if tz not in favorites]

selected_tz = st.sidebar.selectbox("Select Timezone", options=final_tz_list, index=0)

# --- 2. TIME SETUP ---
try:
    tz = pytz.timezone(selected_tz)
except:
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
manual_mode = st.sidebar.checkbox("Manual Time Override")

if manual_mode:
    decimal_time = st.sidebar.slider("Test Time", 0.0, 23.9, float(hour + minute/60))
    h_24 = int(decimal_time)
    m = int((decimal_time % 1) * 60)
    h_12 = h_24 % 12
    h_12 = 12 if h_12 == 0 else h_12
    current_time_string = f"{h_12}.{m:02d}"
else:
    decimal_time = hour + (minute / 60)
    current_time_string = now.strftime("%-I.%M")

# --- 3. LOGIC ---
sleep_s = sleep_start_i.hour + (sleep_start_i.minute / 60)
wake_s = wake_up_i.hour + (wake_up_i.minute / 60)

if decimal_time >= sleep_s or decimal_time < wake_s:
    status, icon = "Sleepy Time", "🌙"
    bg_color = "#1e1b4b" 
    text_color = "#e0e7ff"
    card_bg = "rgba(255, 255, 255, 0.1)"
else:
    status, icon = "Rise & Shine!", "☀️"
    bg_color = "#fef3c7" 
    text_color = "#78350f"
    card_bg = "rgba(255, 255, 255, 0.4)"

# --- 4. CSS (CLEANEST VERSION) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    
    /* HIDE THE ENTIRE TOP BAR COMPLETELY */
    header[data-testid="stHeader"] {{
        visibility: hidden !important;
        height: 0px !important;
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 40px 20px;
        text-align: center;
        max-width: 500px;
        margin: 100px auto 20px auto;
        border: 1px solid rgba(255,255,255,0.2);
    }}

    .icon-div {{ font-size: 100px; margin-bottom: 20px; }}
    .status-label {{ font-size: 42px; font-weight: 700; }}
    .clock-label {{ font-size: 32px; opacity: 0.8; }}
    
    /* Style the fallback button */
    .stButton>button {{
        background-color: transparent !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: {text_color} !important;
        font-size: 20px !important;
        margin-top: 20px !important;
        border-radius: 12px !important;
    }}

    footer {{visibility: hidden !important;}}
    </style>
    """, unsafe_allow_html=True)

# --- 5. UI ---
# The Main Card
st.markdown(f"""
    <div class="glass-card">
        <div class="icon-div">{icon}</div>
        <div class="status-label">{status}</div>
        {"<div class='clock-label'>" + current_time_string + "</div>" if show_clock else ""}
    </div>
    """, unsafe_allow_html=True)

# THE FALLBACK CONTROL BUTTON
# This creates a small button below the card that opens the sidebar
cols = st.columns([1, 1, 1])
with cols[1]:
    if st.button("⚙️ Settings"):
        # This is a trick: in mobile, Streamlit buttons usually 
        # force the UI to refresh/open sidebars if state changes
        st.sidebar.markdown("### ⚙️ Parent Controls Active")

# --- 6. REFRESH ---
if not manual_mode:
    time.sleep(5)
    st.rerun()
