import streamlit as st
import datetime
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr

st.set_page_config(page_title="Silent SOS AI", layout="centered")
st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")
st.write("Boliye 'HELP' ya 'bachao' aur turant SOS bhej degi")

if 'last_heard' not in st.session_state:
    st.session_state.last_heard = ""

def trigger_alert(word):
    st.error(f"🚨 DANGER DETECTED: '{word}'")
    st.error("SOS TRIGGERED!")
    st.success("📍 Location Sent: Pathankot, Punjab")
    st.success("📞 Alert Sent to: +916239719750")
    st.success(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")

audio = mic_recorder(start_prompt="🎤 Boliye HELP", stop_prompt="⏹️ Stop", key='mic')

if audio:
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio["bytes"], language="en-IN")
        st.session_state.last_heard = text
        st.write(f"**Heard:** {text}")
        
        if any(word in text.lower() for word in ["help", "bachao", "save me", "police"]):
            trigger_alert(text)
    except:
        st.warning("Suna nahi... dobara bolo")

st.markdown("---")
if st.button("🚨 TEST ALERT - Click karke dekho", type="secondary"):
    trigger_alert("TEST MODE")

st.markdown("---")
st.write(f"**Last Heard:** {st.session_state.last_heard}")
