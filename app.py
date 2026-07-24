import streamlit as st
import speech_recognition as sr
import threading
st.set_page_config(page_title="Silent SOS AI", layout="wide")

st.markdown("""
<style>
.stApp {background: white; color: black;}
h1 {color: black; font-size: 55px; font-weight: 900; text-align: center;}
.gold {color: #C49A3B; font-weight: bold; text-align: center;}
.tag {border: 2px solid black; border-radius: 25px; padding: 8px 20px; margin: 5px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="gold" style="font-size:24px">SUMMER SCHOOL \'26</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center"><span class="tag">AI FIRST HACKATHON</span></div>', unsafe_allow_html=True)
st.markdown("<h1>Silent SOS AI</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center'>Help Without Saying a Word</h2>", unsafe_allow_html=True)
st.write("*An AI sentinel that silently detects danger and calls for help before a word is spoken.*")
st.markdown('<div style="text-align:center"><span class="tag">AI for Bharat: Governance & Social Impact</span></div>', unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🚨 AI Features")
    
    if 'monitoring' not in st.session_state:
        st.session_state.monitoring = False

    if st.button("▶️ Start AI Monitoring"):
        st.session_state.monitoring = True
        threading.Thread(target=start_monitoring, daemon=True).start()
        st.success("AI Monitoring Started! Mic is listening...")

    if st.button("⏹️ Stop Monitoring"):
        st.session_state.monitoring = False
        st.info("Monitoring Stopped")


        
        # AI Monitoring Function
def start_monitoring():
 r = sr.Recognizer()
 danger_words = ["help", "bachao", "chodo", "madad", "police"]

 with sr.Microphone() as source:
     st.warning("🎤 AI is Listening... Say 'HELP' for emergency")
     while st.session_state.monitoring:
         try:
             audio = r.listen(source, timeout=1)
             text = r.recognize_google(audio, language="en-IN").lower()
                 for word in danger_words:
                    if word in text:
                        st.error(f"🚨 DANGER DETECTED: '{text}'")
                        # Auto PANIC trigger
                        st.error("SOS TRIGGERED!")
                        st.success("📍 Location Sent: Pathankot, Punjab")
                        st.success("📞 Alert Sent to: +916239719750")
                        st.session_state.monitoring = False
                        return                                                          
         except:
             pass
    if st.button("🆘 PANIC BUTTON", type="primary"):
        st.error("SOS TRIGGERED!")
        st.success("📍 Location Sent: Pathankot, Punjab")
        st.success("📞 Alert Sent to: +916239719750")

with col2:
    st.subheader("TEAM DETAILS")
    st.write("**Team Name:** Tech Nova")
    st.write("**College:** Sardar Beant Singh State University")
    st.write("**Members:**")
    st.write("- Jashanpreet Kaur - Team Leader")
    st.write("- Isha Bhardwaj - Team Member")
    st.write("**Contact:** +91 7888738745,6239719750")
    st.write("**Email:** kaurjashanpreet502@gmail.com, ishabhardwaj2526@gmail.com")
