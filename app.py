import streamlit as st
import datetime

st.set_page_config(page_title="Silent SOS AI", layout="centered")
st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")

def trigger_alert():
    st.error("🚨 DANGER DETECTED: 'HELP'")
    st.error("AI NE DANGER WORD PEHCHANA!")
    st.success("📍 Live Location Sent: Pathankot, Punjab")
    st.success("📞 Emergency Contact Alerted: +916239719750")
    st.success(f"⏰ Alert Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.warning("Police aur family ko turant notification bhej di gayi")
    st.balloons()

st.markdown("---")
st.subheader("Demo Mode")

if st.button("🚨 ACTIVATE EMERGENCY SOS", type="primary", use_container_width=True):
    trigger_alert()

st.markdown("---")
st.info("**Kaise kaam karta hai:** \n1. Mic hamesha background me sunta hai 'HELP'/'bachao' \n2. Turant SOS trigger hota hai \n3. Location + SMS + Call auto chale jate hai \n\n*Note: Cloud security ki wajah se demo me button use kiya hai*")
