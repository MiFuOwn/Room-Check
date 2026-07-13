#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// ================= การตั้งค่า Wi-Fi =================
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ================= การตั้งค่า Firebase =================
// นำ API Key จากหน้า Project settings > General ของ Firebase มาใส่
#define API_KEY "YOUR_FIREBASE_API_KEY"

// URL ของ Realtime Database โดยตัด "https://" และ "/" ด้านท้ายออก (ตัวอย่างด้านล่าง)
#define DATABASE_URL "roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// ================= การตั้งค่าขา Sensor (Pins) =================
/* หมายเหตุ: 
 * ESP8266 มีขา Analog (A0) แค่ขาเดียว หากใช้เซนเซอร์ 2 ตัวที่ต้องอ่านค่า Analog
 * อาจต้องใช้ Multiplexer หรือเปลี่ยนเซนเซอร์ตัวนึงเป็น Digital
 * ในโค้ดนี้ สมมติว่า ESP8266 ใช้ Analog อ่านแสง และ Digital อ่านเสียง
 */
#if defined(ESP32)
  #define LIGHT_PIN 34 // ขา Analog สำหรับ LDR
  #define SOUND_PIN 35 // ขา Analog สำหรับ เซนเซอร์เสียง
#elif defined(ESP8266)
  #define LIGHT_PIN A0 // ขา Analog (มีขาเดียว) สำหรับ LDR
  #define SOUND_PIN 5  // ขา D1 (Digital) สำหรับเซนเซอร์เสียง
#endif

unsigned long sendDataPrevMillis = 0;
int timerDelay = 3000; // ส่งข้อมูลทุกๆ 3 วินาที

void setup() {
  Serial.begin(115200);

  // เชื่อมต่อ Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());

  // กำหนดค่า Firebase
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  // Sign up แบบไม่ระบุตัวตน
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase Auth Successful");
  } else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  // กำหนด callback สำหรับการสร้าง token (ต้องมี)
  config.token_status_callback = tokenStatusCallback;
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // กำหนดโหมดให้ขาเซนเซอร์
  #if defined(ESP8266)
    pinMode(SOUND_PIN, INPUT);
  #endif
}

void loop() {
  // ทำงานทุกๆ timerDelay (3 วินาที)
  if (Firebase.ready() && (millis() - sendDataPrevMillis > timerDelay || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();

    int lightValue = 0;
    int soundValue = 0;

    #if defined(ESP32)
      // ESP32 อ่านค่า Analog ได้ 0-4095
      lightValue = analogRead(LIGHT_PIN); 
      soundValue = analogRead(SOUND_PIN);
      
      // แปลงค่าให้เข้ากับ Streamlit (แสง 0-100, เสียง 0-1023)
      lightValue = map(lightValue, 0, 4095, 0, 100);
      soundValue = map(soundValue, 0, 4095, 0, 1023);
      
    #elif defined(ESP8266)
      // ESP8266 อ่านค่า Analog ได้ 0-1023
      lightValue = analogRead(LIGHT_PIN); 
      // แปลงให้เป็น % (0-100)
      lightValue = map(lightValue, 0, 1023, 0, 100);
      
      // อ่านค่า Digital จากเซนเซอร์เสียง (มีเสียง = 1, ไม่มี = 0)
      // นำไปคูณ 1023 เพื่อให้กราฟเด้งไปที่ระดับสูงสุดเวลามีเสียงดัง
      soundValue = digitalRead(SOUND_PIN) * 1023; 
    #endif

    Serial.printf("Light: %d, Sound: %d\n", lightValue, soundValue);

    // อัปเดตข้อมูลขึ้น Firebase
    // /data/Light จะทำให้ url/data.json คืนค่า {"Light": ...}
    if (Firebase.RTDB.setInt(&fbdo, "/data/Light", lightValue)) {
      Serial.println("PASSED: Light value saved.");
    } else {
      Serial.println("FAILED: Light value - " + fbdo.errorReason());
    }

    if (Firebase.RTDB.setInt(&fbdo, "/data/Sound", soundValue)) {
      Serial.println("PASSED: Sound value saved.");
    } else {
      Serial.println("FAILED: Sound value - " + fbdo.errorReason());
    }
    
    Serial.println("------------------------------------");
  }
}
