#include <Wire.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <MPU6050.h>

MPU6050 mpu;
TinyGPSPlus gps;

// Pins
#define BUTTON_PIN 2      // I am Safe button
#define PIR_PIN 3         // Movement sensor
#define GPS_RX 16         // NEO-6M TX
#define GPS_TX 17         // NEO-6M RX  
#define GSM_RX 4          // SIM800L TX
#define GSM_TX 5          // SIM800L RX

SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
SoftwareSerial gsmSerial(GSM_RX, GSM_TX);

String emergencyNumber = "+91XXXXXXXXXX"; // YAHAN APNA NUMBER DALO
float accX, accY, accZ, gyroX, gyroY, gyroZ;
bool fallDetected = false;
unsigned long lastAlert = 0;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(PIR_PIN, INPUT);
  
  Wire.begin();
  mpu.initialize();
  
  gpsSerial.begin(9600);
  gsmSerial.begin(9600);
  
  Serial.println("SafeTrack System Starting...");
  delay(5000);
}

void loop() {
  // 1. GPS Data Update
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
  
  // 2. Fall Detection using MPU6050
  mpu.getMotion6(&accX, &accY, &accZ, &gyroX, &gyroY, &gyroZ);
  float totalAccel = sqrt(accX*accX + accY*accY + accZ*accZ);
  
  if(totalAccel > 2.5 || totalAccel < 0.5) { // Fall threshold
    if(millis() - lastAlert > 10000) { // 10 sec gap
      sendSOS("FALL DETECTED!");
      makeCall();
      lastAlert = millis();
    }
  }
  
  // 3. Movement Detection
  if(digitalRead(PIR_PIN) == HIGH) {
    sendAlert("MOVEMENT DETECTED!");
    delay(5000);
  }
  
  // 4. I am Safe Button
  if(digitalRead(BUTTON_PIN) == LOW) {
    sendAlert("I AM SAFE");
    delay(2000);
  }
  
  delay(100);
}

void sendSOS(String message) {
  String location = getLocation();
  String dateTime = getDateTime();
  String fullMsg = message + "\nTime: " + dateTime + "\nLocation: " + location;
  
  gsmSerial.println("AT+CMGF=1"); delay(500);
  gsmSerial.println("AT+CMGS=\"" + emergencyNumber + "\""); delay(500);
  gsmSerial.print(fullMsg); delay(500);
  gsmSerial.write(26); // Ctrl+Z to send
  Serial.println("SOS Sent: " + fullMsg);
}

void sendAlert(String message) {
  String location = getLocation();
  String fullMsg = message + "\nLocation: " + location;
  
  gsmSerial.println("AT+CMGF=1"); delay(500);
  gsmSerial.println("AT+CMGS=\"" + emergencyNumber + "\""); delay(500);
  gsmSerial.print(fullMsg); delay(500);
  gsmSerial.write(26);
  Serial.println("Alert Sent: " + fullMsg);
}

void makeCall() {
  gsmSerial.println("ATD" + emergencyNumber + ";"); // Call
  delay(20000); // 20 sec ring
  gsmSerial.println("ATH"); // Hang up
}

String getLocation() {
  if(gps.location.isValid()) {
    return "https://maps.google.com/?q=" + 
           String(gps.location.lat(), 6) + "," + 
           String(gps.location.lng(), 6);
  } else {
    return "GPS Not Found";
  }
}

String getDateTime() {
  if(gps.date.isValid() && gps.time.isValid()) {
    String dt = String(gps.date.day()) + "/" + String(gps.date.month()) + "/" + String(gps.date.year());
    dt += " " + String(gps.time.hour()) + ":" + String(gps.time.minute());
    return dt;
  } else {
    return "No Time";
  }
}
