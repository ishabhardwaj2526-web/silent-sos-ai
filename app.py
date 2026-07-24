import streamlit as st
import datetime
import threading
import time
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr

st.set_page_config(page_title="Silent SOS AI", layout="centered")

st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")
st.write("Boliye 'HELP' ya 'bachao' aur turant SOS bhej degi")

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False
if "last_heard" not in st.session_state:
    st.session_state.last_heard = ""

DANGER_WORDS = ["help", "bachao", "save me", "police", "madad"]

def trigger_alert(word):
    st.error(f"🚨 DANGER DETECTED: '{word}'")
    st.error("SOS TRIGGERED!")
    st.success("📍 Location Sent: Pathankot, Punjab")
    st.success("📞 Alert Sent to: +916239719750")
    st.success(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.session_state.alert_sent = True

def listen_loop():
    recognizer = sr.Recognizer()
    while st.session_state.monitoring:
        audio = mic_recorder(start_prompt="🎤 Boliye HELP", stop_prompt="⏹️ Stop", key='mic')
        
        if audio:
            try:
                text = recognizer.recognize_google(audio["bytes"], language="en-IN")
                st.session_state.last_heard = text
                st.write(f"**Heard:** {text}")
                
                for word in DANGER_WORDS:
                    if word in text.lower() and not st.session_state.alert_sent:
                        trigger_alert(word)
                        time.sleep(10)
                        st.session_state.alert_sent = False
            except:
                pass
        time.sleep(0.5)

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start AI Monitoring", type="primary"):
        st.session_state.monitoring = True
        st.session_state.alert_sent = False
        threading.Thread(target=listen_loop, daemon=True).start()

with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.monitoring = False

st.markdown("---")
if st.button("🚨 TEST ALERT - Click karke dekho", type="secondary"):
    trigger_alert("TEST MODE")

st.markdown("---")
if st.session_state.monitoring:
    st.info("✅ AI is Active and Listening...")
    st.write(f"**Last Heard:** {st.session_state.last_heard}")
else:
    st.warning("🔴 AI is Idle. Press Start to begin.")
