package com.example.silentsos

import android.Manifest
import android.app.*
import android.content.*
import android.content.pm.PackageManager
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.location.Location
import android.os.*
import android.speech.RecognizerIntent
import android.telephony.SmsManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.*
import java.util.*

class MainActivity : AppCompatActivity(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private val emergencyNumbers = arrayOf("9988776655") // APNA NUMBER
    private var lastAccel = 0f
    private var lastGyro = 0f
    private var fallCooldown = 0L
    private val SPEECH_REQUEST_CODE = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        requestPermissions()

        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)

        // Buttons
        findViewById<Button>(R.id.btnEmergency).setOnClickListener { startDetection() }
        findViewById<Button>(R.id.btnSafe).setOnClickListener { sendSOS("I AM SAFE") }
        findViewById<Button>(R.id.btnSettings).setOnClickListener { openSettings() }

        // Voice trigger
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Say 'HELP' for emergency")
        startActivityForResult(intent, SPEECH_REQUEST_CODE)
    }

    private fun startDetection() {
        sensorManager.registerListener(this, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_NORMAL)
        sensorManager.registerListener(this, sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE), SensorManager.SENSOR_DELAY_NORMAL)
        Toast.makeText(this, "AI Detection ON", Toast.LENGTH_SHORT).show()
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (System.currentTimeMillis() - fallCooldown < 8000) return

        if (event?.sensor?.type == Sensor.TYPE_ACCELEROMETER) {
            val acceleration = kotlin.math.sqrt(event.values[0]*event.values[0] + event.values[1]*event.values[1] + event.values[2]*event.values[2])
            if (acceleration > 18) { // Fall
                fallCooldown = System.currentTimeMillis()
                sendSOS("FALL DETECTED AUTO")
            }
        }
        if (event?.sensor?.type == Sensor.TYPE_GYROSCOPE) {
            val rotation = kotlin.math.abs(event.values[0]) + kotlin.math.abs(event.values[1]) + kotlin.math.abs(event.values[2])
            if (rotation > 5) { // Movement
                fallCooldown = System.currentTimeMillis()
                sendSOS("MOVEMENT DETECTED AUTO")
            }
        }
    }

    private fun sendSOS(type: String) {
        fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
            val loc = if (location!= null) "https://maps.google.com/?q=${location.latitude},${location.longitude}" else "Location Off"
            val battery = getBatteryLevel()
            val message = "🚨 $type 🚨\nLocation: $loc\nBattery: $battery%\nTime: ${System.currentTimeMillis()}"
            for (number in emergencyNumbers) {
                SmsManager.getDefault().sendTextMessage(number, null, message, null, null)
            }
            Toast.makeText(this, "SOS Sent: $type", Toast.LENGTH_SHORT).show()
        }
    }

    private fun getBatteryLevel(): Int {
        val batteryIntent = registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val level = batteryIntent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)?: -1
        val scale = batteryIntent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1)?: -1
        return (level * 100 / scale.toFloat()).toInt()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == SPEECH_REQUEST_CODE && resultCode == RESULT_OK) {
            val results = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if (results?.get(0)?.toUpperCase() == "HELP") {
                sendSOS("HELP DETECTED VIA VOICE")
            }
        }
        super.onActivityResult(requestCode, resultCode, data)
    }

    private fun requestPermissions() {
        ActivityCompat.requestPermissions(this, arrayOf(
            Manifest.permission.SEND_SMS, Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.RECORD_AUDIO
        ), 100)
    }
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
}
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="24dp"
    android:gravity="center">

    <TextView android:text="🚨 Silent SOS AI" android:textSize="28sp" android:textStyle="bold"/>
    <TextView android:text="Level 2 Features" android:layout_marginBottom="30dp"/>

    <Button android:id="@+id/btnEmergency" android:layout_width="match_parent" android:layout_height="60dp"
        android:text="🔴 AI POWER EMERGENCY ON" android:backgroundTint="#D32F2F" android:textColor="#FFF" />
    <Button android:id="@+id/btnSafe" android:layout_width="match_parent" android:layout_height="50dp"
        android:text="✅ I AM SAFE" android:backgroundTint="#4CAF50" android:textColor="#FFF" android:layout_marginTop="15dp"/>
    <Button android:id="@+id/btnSettings" android:layout_width="match_parent" android:layout_height="50dp"
        android:text="⚙️ Settings" android:layout_marginTop="15dp"/>
</LinearLayout>s
