import streamlit as st
from datetime import datetime
import time

# 1. Get current hour
now = datetime.now()
current_hour = now.hour
current_time = now.strftime("%H:%M:%S")

# 2. Define logic for colors and images
if 5 <= current_hour < 12:
    status = "Morning"
    bg_color = "#FFFAE0"  # Soft yellow
    img_url = "https://example.com/sunrise.jpg"
elif 12 <= current_hour < 18:
    status = "Afternoon"
    bg_color = "#E0F7FA"  # Sky blue
    img_url = "https://example.com/sun.jpg"
else:
    status = "Night"
    bg_color = "#2C3E50"  # Dark blue/grey
    img_url = "https://example.com/moon.jpg"

# 3. Inject Custom CSS for background color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Display the content
st.title(f"Good {status}!")
st.header(f"The time is {current_time}")
st.image(img_url, caption=f"Current vibe: {status}")

# 5. Optional: Auto-refresh every minute
# time.sleep(60)
# st.rerun()
