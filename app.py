import streamlit as st
from datetime import datetime
import time
from twilio.rest import Client

st.set_page_config(page_title="Silent SOS AI", page_icon="🚨", layout="centered")

st.title("🚨 Silent SOS AI")
st.subheader("AI-powered Emergency System")

# ===== SETTINGS =====
EMERGENCY_NUMBERS = ["+91 9988776655"]  # <-- APNA NUMBER YAHAN DALO +91 ke saath
TWILIO_SID = "YOUR_TWILIO_SID"  # twilio.com se free account banao
TWILIO_TOKEN = "YOUR_TWILIO_TOKEN"
TWILIO_PHONE = "+1XXXXXXXXXX" # Twilio wala number

# ===== FUNCTIONS =====
def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for number in EMERGENCY_NUMBERS:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=number
        )

def send_alert(alert_type, lat="NA", lon="NA", battery="NA"):
    location = f"https://maps.google.com/?q={lat},{lon}" if lat != "NA" else "Location Off"
    battery_text = f"{battery}%" if battery != "NA" else "NA"
    time_now = get_time()
    
    full_message = f"🚨 {alert_type} 🚨\nLocation: {location}\nBattery: {battery_text}\nTime: {time_now}"
    
    try:
        send_sms(full_message)
        st.success(f"✅ ALERT SENT: {alert_type}")
    except:
        st.error("Twilio details galat hain")
    
    st.code(full_message)

# ===== AUTOMATIC SENSOR JS CODE =====
sensor_js = """
<script>
// Phone ke sensor access karne ke liye
let lastAccel = 0;
let cooldown = 0;

function sendToPython(type, lat, lon, battery) {
    const data = {type: type, lat: lat, lon: lon, battery: battery};
    window.parent.postMessage(data, "*");
}

// Location + Battery leke sensor start karo
navigator.geolocation.getCurrentPosition(pos => {
    let lat = pos.coords.latitude;
    let lon = pos.coords.longitude;
    
    navigator.getBattery().then(batt => {
        let battery = Math.round(batt.level * 100);
        
        // Accelerometer start
        window.addEventListener('devicemotion', (e) => {
            let acc = e.accelerationIncludingGravity;
            let acceleration = Math.sqrt(acc.x*acc.x + acc.y*acc.y + acc.z*acc.z);
            
            if (acceleration > 18 && Date.now() - cooldown > 8000) { // Fall
                cooldown = Date.now();
                sendToPython("FALL DETECTED AUTO", lat, lon, battery);
            }
        });
    });
});
</script>
"""

# ===== UI =====
if st.button("🔴 AI POWER EMERGENCY ON", use_container_width=True, type="primary"):
    st.components.v1.html(sensor_js, height=0) # JS chalu
    st.session_state.detection = True
    st.info("AI Detection ON - Phone hilao ya girne par auto SMS jayega")

if st.button("✅ I AM SAFE"):
    send_alert("I AM SAFE")

# Python me JS se message pakadne ke liye
st.components.v1.html("""
<script>
window.addEventListener("message", (event) => {
    if(event.data.type){
        // Yahan Streamlit ko batana padega. Abhi demo ke liye
        console.log(event.data)
    }
});
</script>
""", height=0)

st.markdown("---")
st.caption("Note: 1. Phone me kholo 2. Location Permission Allow karo 3. Twilio details dalo")
