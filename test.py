from firebase_config import db

db.collection("devices").document("DEVICE_001").set({
    "mq6": 320
})

print("Data stored")