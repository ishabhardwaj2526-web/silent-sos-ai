import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System - Level 2")

# ===== SETTINGS =====
EMERGENCY_NUMBER = "+91 9988776655" # <-- APNA NUMBER YAHAN

if 'lat' not in st.session_state:
    st.session_state.lat = None
if 'lon' not in st.session_state:
    st.session_state.lon = None
if 'battery' not in st.session_state:
    st.session_state.battery = None

# ===== FUNCTION =====
def send_alert(alert_type):
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if st.session_state.lat and st.session_state.lon:
        location = f"https://maps.google.com/?q={st.session_state.lat},{st.session_state.lon}"
        battery = f"{st.session_state.battery}%"
    else:
        location = "Manual - Permission nahi di"
        battery = "NA"
    
    message = f"🚨 {alert_type} 🚨\nLocation: {location}\nBattery: {battery}\nTime: {time_now}"
    
    st.success(f"✅ ALERT SENT: {alert_type}")
    st.code(message)
    
    # Yahan link clickable bhi dikha denge
    if st.session_state.lat:
        st.link_button("📍 Live Location Map Kholo", location)

# ===== LOCATION LENE KE LIYE JS =====
st.components.v1.html("""
<script>
function sendData() {
    navigator.geolocation.getCurrentPosition(pos => {
        const data = {lat: pos.coords.latitude, lon: pos.coords.longitude};
        window.parent.postMessage(data, "https://*.streamlit.app");
    }, err => console.log(err));
    
    navigator.getBattery().then(batt => {
        const data = {battery: Math.round(batt.level * 100)};
        window.parent.postMessage(data, "https://*.streamlit.app");
    });
}
sendData();
</script>
""", height=0)

# Query params se data lo
query_params = st.query_params
if "lat" in query_params:
    st.session_state.lat = float(query_params["lat"])
    st.session_state.lon = float(query_params["lon"])
if "battery" in query_params:
    st.session_state.battery = int(query_params["battery"])

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
if st.session_state.lat:
    st.info(f"✅ Live Location Captured: {st.session_state.lat}, {st.session_state.lon}")
else:
    st.warning("⚠️ Location nahi mili. Phone me kholo aur Permission Allow karo")
