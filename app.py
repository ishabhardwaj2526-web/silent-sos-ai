import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime

st.set_page_config(page_title="Silent SOS AI", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System")

# 1. LOCATION LENE KA CODE
st.write("### 📍 Live Location")
location = streamlit_geolocation() # ye permission popup dega

if location and location['latitude']:
    lat = location['latitude']
    lon = location['longitude']
    st.success(f"Location: {lat:.5f}, {lon:.5f}")
else:
    st.warning("Location: Not available (need permission). Upar 'Allow' dabao")

# 2. BATTERY - Web pe nahi milegi
st.write("### 🔋 Battery")
st.info("Battery: Not available (browser limitation)")

# 3. TIME
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.write(f"### ⏰ Time: {now}")

# 4. BUTTONS
col1, col2 = st.columns(2)
with col1:
    if st.button("FALL DETECTED", type="primary"):
        st.error(f"FALL DETECTED ALERT!\n\nTime: {now}\n\nLocation: {lat:.5f}, {lon:.5f}" if location else "Location not available")
with col2:
    if st.button("MOVEMENT DETECTED"):
        st.warning(f"MOVEMENT DETECTED ALERT!\n\nTime: {now}\n\nLocation: {lat:.5f}, {lon:.5f}" if location else "Location not available")

if st.button("I AM SAFE", type="secondary"):
    st.success("You are marked SAFE ✅")
