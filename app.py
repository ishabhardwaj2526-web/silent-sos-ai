import streamlit as st
import datetime
import speech_recognition as sr
from streamlit_mic_recorder import speech_recorder

st.set_page_config(page_title="Silent SOS AI", layout="centered")
st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")

def trigger_alert(word):
    st.error(f"🚨 DANGER DETECTED: '{word}'")
    st.success("📍 Location Sent: Pathankot, Punjab")
    st.success("📞 Alert Sent to: +916239719750")
    st.success(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.balloons()

st.subheader("🎤 Voice Detection")
audio = speech_recorder(language="en", use_container_width=True)

if audio:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio) as source:
            data = r.record(source)
        text = r.recognize_google(data, language="en")
        st.write(f"Heard: {text}")
        if "help" in text.lower():
            trigger_alert(text)
    except:
        st.warning("Suna nahi... dobara bolo")

st.markdown("---")
st.subheader("Demo Button")
if st.button("🚨 TEST EMERGENCY ALERT", type="primary", use_container_width=True):
    trigger_alert("HELP")
