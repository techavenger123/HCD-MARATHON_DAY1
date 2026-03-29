#include <Adafruit_Fingerprint.h>

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial1);

uint8_t id;

void setup() {
  Serial.begin(115200);
  Serial1.begin(57600);

  delay(2000);

  Serial.println("\n=== REGISTER DEVICE FINGERPRINT ===");

  if (!finger.verifyPassword()) {
    Serial.println("❌ Sensor NOT found");
    while (1);
  }

  Serial.println("Enter Device ID (example: 3 for device3):");

  while (!Serial.available());
  id = Serial.parseInt();

  if (id < 1 || id > 127) {
    Serial.println("❌ Invalid ID");
    return;
  }

  Serial.print("Registering device");
  Serial.println(id);

  enrollFingerprint();
}

void enrollFingerprint() {

  int p;

  Serial.println("Place finger...");

  while (finger.getImage() != FINGERPRINT_OK) delay(200);

  if (finger.image2Tz(1) != FINGERPRINT_OK) {
    Serial.println("Error");
    return;
  }

  Serial.println("Remove finger...");
  delay(2000);

  while (finger.getImage() != FINGERPRINT_NOFINGER);

  Serial.println("Place same finger again...");

  while (finger.getImage() != FINGERPRINT_OK) delay(200);

  if (finger.image2Tz(2) != FINGERPRINT_OK) {
    Serial.println("Error");
    return;
  }

  if (finger.createModel() != FINGERPRINT_OK) {
    Serial.println("Finger mismatch");
    return;
  }

  if (finger.storeModel(id) == FINGERPRINT_OK) {
    Serial.println("✅ Stored successfully!");
  } else {
    Serial.println("❌ Store failed");
  }
}

void loop() {}