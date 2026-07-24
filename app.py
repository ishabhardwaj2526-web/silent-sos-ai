import streamlit as st

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
    if st.button("▶️ Start AI Monitoring"):
        st.info("AI is Listening for 'Help'...")
    if st.button("🆘 PANIC BUTTON", type="primary"):
        st.error("SOS TRIGGERED!")
        st.success("📍 Location Sent: Pathankot, Punjab")
        st.success("📞 Alert Sent to: +91 7888738745")

with col2:
    st.subheader("TEAM DETAILS")
    st.write("**Team Name:** Tech Nova")
    st.write("**College:** Sardar Beant Singh State University")
    st.write("**Members:**")
    st.write("- Jashanpreet Kaur - Team Leader")
    st.write("- Isha Bhardwaj - Team Member")
    st.write("**Contact:** +91 7888738745,6239719750")
    st.write("**Email:** kaurjashanpreet502@gmail.com, ishabhardwaj2526@gmail.com")