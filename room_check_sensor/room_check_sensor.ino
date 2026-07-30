#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"
#include "secrets.h"   // WIFI_SSID, WIFI_PASSWORD, API_KEY, DATABASE_URL, ROOM_ID

#if defined(ESP32)
  #define LIGHT_PIN 34
  #define SOUND_PIN 35
#elif defined(ESP8266)
  #define LIGHT_PIN A0
  #define SOUND_PIN 5
#endif

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

const unsigned long SEND_INTERVAL_MS = 3000;
unsigned long lastSendMs = 0;

bool wifiConnect(unsigned long timeoutMs) {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > timeoutMs) {
      Serial.println("\nWi-Fi connect timed out, will retry in loop().");
      return false;
    }
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(200);

  wifiConnect(20000);

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase auth OK");
  } else {
    Serial.printf("Firebase auth failed: %s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  #if defined(ESP8266)
    pinMode(SOUND_PIN, INPUT);
  #endif
}

void loop() {
  if (!Firebase.ready()) return;
  if (millis() - lastSendMs < SEND_INTERVAL_MS && lastSendMs != 0) return;
  lastSendMs = millis();

  int lightValue = 0;
  int soundValue = 0;

  #if defined(ESP32)
    lightValue = analogRead(LIGHT_PIN);
    soundValue = analogRead(SOUND_PIN);
    lightValue = map(lightValue, 0, 4095, 0, 100);
    soundValue = map(soundValue, 0, 4095, 0, 1023);
  #elif defined(ESP8266)
    lightValue = analogRead(LIGHT_PIN);
    lightValue = map(lightValue, 0, 1023, 0, 100);
    soundValue = digitalRead(SOUND_PIN) * 1023;
  #endif

  Serial.printf("[%s] Light: %d, Sound: %d\n", ROOM_ID, lightValue, soundValue);

  String basePath = String("/rooms/") + ROOM_ID;

  FirebaseJson json;
  json.set("light", lightValue);
  json.set("sound", soundValue);
  json.set("updated_at", (int)(millis()));

  if (Firebase.RTDB.updateNode(&fbdo, basePath.c_str(), &json)) {
    Serial.println("PASSED: reading saved.");
  } else {
    Serial.println("FAILED: " + fbdo.errorReason());
  }
}