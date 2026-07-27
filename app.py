import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System")

def send_alert(alert_type):
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.success(f"✅ {alert_type} ALERT!")
    st.write(f"**Time:** {time_now}")
    st.write("**Location:** Not available (need permission)")
    st.write("**Battery:** Not available (browser limitation)")

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
st.caption("Note: Phone me kholo to location permission do")
