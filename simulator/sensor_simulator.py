import random
from datetime import datetime
import time
import json
from kafka import KafkaProducer


# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

topic_name = "telemetry-data"


# Container details
containers = [
    {"container_id": "C001", "product": "Avocado"},
    {"container_id": "C002", "product": "Mango"},
    {"container_id": "C003", "product": "Banana"},
    {"container_id": "C004", "product": "Orange"},
    {"container_id": "C005", "product": "Grapes"}
]


# Generate telemetry continuously
while True:

    selected_container = random.choice(containers)

    telemetry = {
        "container_id": selected_container["container_id"],
        "product": selected_container["product"],
        "temperature": round(random.uniform(2.0, 8.0), 1),
        "moisture": random.randint(75, 95),
        "air_pressure": random.randint(1008, 1018),
        "vibration": round(random.uniform(0.0, 5.0), 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "distance_remaining_km": random.randint(10, 300)
    }


    # Send telemetry data to Kafka
    producer.send(topic_name, telemetry)

    print("Sent to Kafka:", telemetry)


    # Send data every 2 seconds
    time.sleep(2)