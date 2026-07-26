#include <Wire.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <MPU6050.h>

MPU6050 mpu;
TinyGPSPlus gps;

// ==== SETTINGS ===
String emergencyNumber = "+91XXXXXXXXXX"; // <-- APNA NUMBER YAHAN DALO
// ==================

// Pins for ESP32
HardwareSerial gpsSerial(1); // GPS: RX=16, TX=17
HardwareSerial gsmSerial(2); // GSM: RX=4, TX=5
#define PIR_PIN 3
#define BUTTON_PIN 2

float ax, ay, az, gx, gy, gz;
unsigned long lastAlert = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  
  pinMode(PIR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);
  gsmSerial.begin(9600, SERIAL_8N1, 4, 5);
  
  Serial.println("SafeTrack System ON");
  delay(5000);
}

void loop() {
  // GPS Read
  while (gpsSerial.available() > 0) gps.encode(gpsSerial.read());
  
  // 1. FALL DETECTION
  mpu.getAcceleration(&ax, &ay, &az);
  float totalG = sqrt(ax*ax + ay*ay + az*az) / 16384.0; // convert to g
  
  if((totalG > 2.0 || totalG < 0.5) && millis() - lastAlert > 10000) {
    sendSOS("FALL DETECTED!");
    makeCall();
    lastAlert = millis();
  }
  
  // 2. MOVEMENT DETECTION
  if(digitalRead(PIR_PIN) == HIGH) {
    sendAlert("MOVEMENT DETECTED!");
    delay(5000);
  }
  
  // 3. I AM SAFE BUTTON
  if(digitalRead(BUTTON_PIN) == LOW) {
    sendAlert("I AM SAFE");
    delay(2000);
  }
  
  delay(200);
}

void sendSOS(String msg) {
  String fullMsg = msg + "\nTime: " + getTime() + "\nLoc: " + getLocation();
  gsmSerial.println("AT+CMGF=1"); delay(500);
  gsmSerial.println("AT+CMGS=\"" + emergencyNumber + "\""); delay(500);
  gsmSerial.print(fullMsg); delay(500);
  gsmSerial.write(26);
}

void sendAlert(String msg) {
  String fullMsg = msg + "\nLoc: " + getLocation();
  gsmSerial.println("AT+CMGF=1"); delay(500);
  gsmSerial.println("AT+CMGS=\"" + emergencyNumber + "\""); delay(500);
  gsmSerial.print(fullMsg); delay(500);
  gsmSerial.write(26);
}

void makeCall() {
  gsmSerial.println("ATD" + emergencyNumber + ";");
  delay(20000);
  gsmSerial.println("ATH");
}

String getLocation() {
  if(gps.location.isValid())
    return "https://maps.google.com/?q=" + String(gps.location.lat(),6) + "," + String(gps.location.lng(),6);
  else return "GPS Waiting...";
}

String getTime() {
  if(gps.date.isValid() && gps.time.isValid())
    return String(gps.date.day()) + "/" + String(gps.date.month()) + " " + String(gps.time.hour()) + ":" + String(gps.time.minute());
  else return "No Time";
}
