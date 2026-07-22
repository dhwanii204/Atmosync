from kafka import KafkaConsumer
import json


# Kafka topic details
TOPIC_NAME = "fruit_telemetry"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers="127.0.0.1:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)


def calculate_spoilage_risk(data):
    temperature = data["temperature"]
    moisture = data["moisture"]
    vibration = data["vibration"]

    # Risk calculation logic
    if temperature > 7 or moisture > 90 or vibration > 4:
        risk = "HIGH"
    elif temperature > 5 or moisture > 85 or vibration > 2.5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk


print("Analytics processor started...")

for message in consumer:
    telemetry = message.value

    telemetry["spoilage_risk"] = calculate_spoilage_risk(telemetry)

    print("Processed Telemetry:")
    print(json.dumps(telemetry, indent=4))
    print("-" * 50)
    