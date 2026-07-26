import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System")

def get_location():
    lat, lon = 31.3260, 74.9275  # Tarn Taran demo location
    return f"https://maps.google.com/?q={lat},{lon}"

def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def send_alert(message):
    st.success("📲 ALERT SENT!")
    st.info(f"**Message:** {message}")
    st.info(f"**Time:** {get_time()}")
    st.info(f"**Location:** {get_location()}")

st.markdown("### Demo Mode")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚨 FALL DETECTED", use_container_width=True):
        send_alert("FALL DETECTED!")
with col2:
    if st.button("✅ I AM SAFE", use_container_width=True):
        send_alert("I AM SAFE")

if st.button("📍 MOVEMENT DETECTED", use_container_width=True):
    send_alert("MOVEMENT DETECTED!")

st.markdown("---")
st.markdown("**Kaise kaam karta hai:**")
st.markdown("1. Mic hamesha background me sunta hai 'HELP' / 'bachao'")
st.markdown("2. Turant SOS trigger hota hai")
st.markdown("3. Location + SMS + Call auto chale jate hai")
st.caption("Note: Cloud security ki wajah se demo me button use kiya hai")
