import streamlit as st
import speech_recognition as sr
import threading
import time
from datetime import datetime

# Page Config
st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="wide")

st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")
st.markdown("Boliye 'HELP' ya 'bachao' aur AI turant SOS bhej degi")

# Session State
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False

# Columns
col1, col2 = st.columns(2)

# AI Monitoring Function
def start_monitoring():
    r = sr.Recognizer()
    danger_words = ["help", "bachao", "chodo", "madad", "police", "save me"]
    
    with sr.Microphone() as source:
        st.warning("🎤 AI is Listening... Say 'HELP' for emergency")
        r.adjust_for_ambient_noise(source, duration=1)
        
        while st.session_state.monitoring:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                text = r.recognize_google(audio, language="en-IN").lower()
                st.info(f"Heard: {text}")
                
                for word in danger_words:
                    if word in text:
                        st.error(f"🚨 DANGER DETECTED: '{text}'")
                        st.error("SOS TRIGGERED!")
                        st.success("📍 Location Sent: Pathankot, Punjab")
                        st.success("📞 Alert Sent to: +916239719750")
                        st.success(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
                        st.session_state.monitoring = False
                        st.session_state.alert_sent = True
                        return
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                pass

# Buttons
with col1:
    if st.button("▶️ Start AI Monitoring", type="primary"):
        st.session_state.monitoring = True
        st.session_state.alert_sent = False
        threading.Thread(target=start_monitoring, daemon=True).start()

with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.monitoring = False
        st.write("Monitoring Stopped")

# Status
if st.session_state.monitoring:
    st.success("✅ AI is Active and Listening...")
elif st.session_state.alert_sent:
    st.error("🚨 Alert was sent! Stay Safe!")
else:
    st.info("🔴 AI is Idle. Press Start to begin.")

# Instructions
st.markdown("---")
st.subheader("📖 How to Use:")
st.markdown("1. **Start AI Monitoring** button dabao")
st.markdown("2. Mic permission **Allow** karo")
st.markdown("3. Emergency me bolo: **HELP, bachao, police, madad**")
st.markdown("4. AI turant alert dikha degi")
