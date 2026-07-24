import streamlit as st
import datetime

st.set_page_config(page_title="Silent SOS AI", layout="centered")
st.title("🚨 Silent SOS AI")
st.markdown("**AI-powered Emergency Detection System**")
st.write("Demo: Text me 'HELP' likho ya neeche button dabao")

def trigger_alert(word):
    st.error(f"🚨 DANGER DETECTED: '{word}'")
    st.error("AI NE SOS TRIGGER KIYA!")
    st.success("📍 Location Sent: Pathankot, Punjab")
    st.success("📞 Alert Sent to: +916239719750")
    st.success(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.balloons()

word = st.text_input("Yaha 'HELP' ya 'bachao' type karo:")
if st.button("Check karo"):
    if any(w in word.lower() for w in ["help", "bachao", "save me"]):
        trigger_alert(word)
    else:
        st.info(f"Safe: '{word}'")

st.markdown("---")
if st.button("🚨 TEST EMERGENCY ALERT", type="primary"):
    trigger_alert("HELP")
