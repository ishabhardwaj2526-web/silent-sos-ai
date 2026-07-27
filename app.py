import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System - Level 2")

# ===== SETTINGS =====
EMERGENCY_NUMBER = "+91 9988776655" # <-- APNA NUMBER YAHAN DALO

# ===== FUNCTIONS =====
def send_alert(alert_type, location="Manual"):
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    battery = "Browser se nahi milta" 
    
    # Agar phone hai to real location lega
    if st.session_state.get('lat'):
        location = f"https://maps.google.com/?q={st.session_state.lat},{st.session_state.lon}"
        battery = f"{st.session_state.battery}%"
    
    message = f"🚨 {alert_type} 🚨\nLocation: {location}\nBattery: {battery}\nTime: {time_now}"
    
    st.success(f"✅ ALERT SENT: {alert_type}")
    st.code(message)
    st.info(f"SMS jayega: {EMERGENCY_NUMBER}")

# ===== LOCATION + SENSOR KE LIYE JS =====
location_js = """
<script>
// Phone me location + battery lene ke liye
navigator.geolocation.getCurrentPosition(pos => {
    window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*");
});
navigator.getBattery().then(batt => {
    window.parent.postMessage({battery: Math.round(batt.level * 100)}, "*");
});
</script>
"""
st.components.v1.html(location_js, height=0)

# JS se data pakdo
st.components.v1.html("""
<script>
window.addEventListener("message", (event) => {
    if(event.data.lat) { window.streamlitData = {lat: event.data.lat, lon: event.data.lon}; }
    if(event.data.battery) { window.streamlitData = {...window.streamlitData, battery: event.data.battery}; }
});
</script>
""", height=0)

# ===== UI =====
st.markdown("### Level 2 Controls")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚨 FALL DETECTED", use_container_width=True, type="primary"):
        send_alert("FALL DETECTED")

with col2:
    if st.button("📍 MOVEMENT DETECTED", use_container_width=True):
        send_alert("MOVEMENT DETECTED")

if st.button("✅ I AM SAFE", use_container_width=True):
    send_alert("I AM SAFE")

st.markdown("---")
st.warning("**Note:** Automatic fall detect phone me bhi manual dabana padega. Browser auto sensor allow nahi karta.")
st.caption("1. Phone me Chrome se kholo 2. Location Permission Allow karo 3. Twilio lagane se real SMS jayega")
