#include <Adafruit_Fingerprint.h>
#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

// ================= WIFI =================
#define WIFI_SSID "WIFI"
#define WIFI_PASSWORD "12345678"

// 🔥 SET YOUR DEVICE ID HERE
#define DEVICE_ID 3  

char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASSWORD;

char server[] = "mq6-monitor-default-rtdb.asia-southeast1.firebasedatabase.app";

WiFiSSLClient wifi;
HttpClient client = HttpClient(wifi, server, 443);

// ================= FINGERPRINT =================
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial1);

// ================= MQ6 + BUZZER + VALVE =================
int mq6Pin = A0;
int buzzerPin = 10;
int valvePin = 9;

bool isAuthorized = false;
int currentFingerID = -1;

// ================= BUZZER TIMING =================
unsigned long lastBeepTime = 0;

// ================= FIREBASE AUTH =================
bool checkAuthorization(int fingerID) {

  String key = "\"device" + String(DEVICE_ID) + "\":true";

  client.get("/users.json");

  String response = client.responseBody();
  client.stop();

  // 🔥 Only allow if fingerprint matches THIS device
  if (response.indexOf(key) != -1 && fingerID == DEVICE_ID) {
    return true;
  }

  return false;
}

// ================= BUZZER FUNCTIONS =================
void buzzerIdle() {
  if (millis() - lastBeepTime >= 3000) {
    digitalWrite(buzzerPin, LOW);
    delay(200);
    digitalWrite(buzzerPin, HIGH);
    lastBeepTime = millis();
  }
}

void buzzerUnauthorized() {
  digitalWrite(buzzerPin, LOW);
  delay(2000);
  digitalWrite(buzzerPin, HIGH);
}

void buzzerAuthorized() {
  for (int i = 0; i < 2; i++) {
    digitalWrite(buzzerPin, LOW);
    delay(500);
    digitalWrite(buzzerPin, HIGH);
    delay(500);
  }
}

// ================= SETUP =================
void setup() {
  Serial.begin(115200);
  Serial1.begin(57600);

  pinMode(buzzerPin, OUTPUT);
  pinMode(valvePin, OUTPUT);

  digitalWrite(buzzerPin, HIGH);
  digitalWrite(valvePin, LOW);

  delay(2000);

  if (!finger.verifyPassword()) {
    Serial.println("❌ Fingerprint sensor not found");
    while (1);
  }

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(2000);
  }

  Serial.println("✅ System Ready");
}

// ================= LOOP =================
void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, pass);
    delay(2000);
    return;
  }

  int gasValue = analogRead(mq6Pin);

  // -------- AUTH --------
  if (!isAuthorized) {

    int p = finger.getImage();

    if (p == FINGERPRINT_NOFINGER) {
      buzzerIdle();
    }

    else if (p == FINGERPRINT_OK) {

      int fingerID = getFingerprintID();

      if (fingerID != -1) {

        Serial.print("Detected ID: ");
        Serial.println(fingerID);

        if (checkAuthorization(fingerID)) {

          Serial.println("✅ Authorized");

          isAuthorized = true;
          currentFingerID = fingerID;

          digitalWrite(valvePin, HIGH);
          buzzerAuthorized();

        } else {

          Serial.println("❌ Unauthorized");

          currentFingerID = -1;
          isAuthorized = false;

          buzzerUnauthorized();
        }
      }
    }
  }

  // -------- ALWAYS UPDATE SAME DEVICE --------
  String path = "/devices/device" + String(DEVICE_ID) + ".json";

  String data = "{";
  data += "\"mq6\":" + String(gasValue) + ",";
  data += "\"finger_id\":" + String(currentFingerID) + ",";
  data += "\"authorized\":" + String(isAuthorized ? "true" : "false");
  data += "}";

  client.put(path, "application/json", data);

  Serial.println("\n===== DEVICE DATA =====");
  Serial.println(data);

  client.stop();

  delay(500);
}

// ================= FINGER =================
int getFingerprintID() {

  if (finger.image2Tz(1) != FINGERPRINT_OK) return -1;

  if (finger.fingerSearch() == FINGERPRINT_OK) {
    return finger.fingerID;
  }

  return -1;
}