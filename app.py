import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System")

# ===== SETTINGS =====
EMERGENCY_NUMBERS = ["+91 9988776655"]  # <-- APNA NUMBER YAHAN DALO
TWILIO_SID = "YOUR_TWILIO_SID"  # SMS bhejne ke liye. Free me trial milta
TWILIO_TOKEN = "YOUR_TWILIO_TOKEN"
TWILIO_PHONE = "+1XXXXXXXXXX"

# ===== FUNCTIONS =====
def get_location():
    # Real browser location ke liye
    return "Browser se permission mangega" 
    # Demo ke liye: Tarn Taran
    # lat, lon = 31.3260, 74.9275
    # return f"https://maps.google.com/?q={lat},{lon}"

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_battery():
    # Browser battery API nahi deta, isliye manual
    return "Browser me available nahi"

def send_alert(message):
    location = get_location()
    battery = get_battery()
    time_now = get_time()
    
    full_message = f"🚨 {message} 🚨\nLocation: {location}\nBattery: {battery}\nTime: {time_now}"
    
    st.success("✅ ALERT SENT!")
    st.code(full_message) # Abhi screen par dikhayega
    st.info("Note: Real SMS ke liye Twilio connect karna padega")
    
    # TODO: Yahan Twilio SMS code lagega

# ===== UI BUTTONS =====
st.markdown("### Demo Mode")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 AI POWER EMERGENCY ON", use_container_width=True, type="primary"):
        st.session_state.detection = True
        st.rerun()

with col2:
    if st.button("✅ I AM SAFE", use_container_width=True):
        send_alert("I AM SAFE")

if st.session_state.get('detection', False):
    st.warning("AI Detection ON - Background monitoring active")
    
    if st.button("🚨 FALL DETECTED"):
        send_alert("FALL DETECTED")
    
    if st.button("📍 MOVEMENT DETECTED"):
        send_alert("MOVEMENT DETECTED")

st.markdown("---")
st.caption("**Level 2 Features:** Fall, Movement, Location, Battery, Time")
