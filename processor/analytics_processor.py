from kafka import KafkaConsumer
import json
import psycopg2


TOPIC_NAME = "fruit_telemetry"


# PostgreSQL connection
connection = psycopg2.connect(
    host="localhost",
    database="atmosync",
    user="postgres",
    password="1920",
    port="5432"
)

cursor = connection.cursor()


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

    if temperature > 7 or moisture > 90 or vibration > 4:
        return "HIGH"

    elif temperature > 5 or moisture > 85 or vibration > 2.5:
        return "MEDIUM"

    else:
        return "LOW"


print("Analytics processor started...")


for message in consumer:

    telemetry = message.value

    telemetry["spoilage_risk"] = calculate_spoilage_risk(telemetry)


    cursor.execute(
        """
        INSERT INTO telemetry
        (
            container_id,
            product,
            temperature,
            moisture,
            air_pressure,
            vibration,
            timestamp,
            distance_remaining_km,
            spoilage_risk
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            telemetry["container_id"],
            telemetry["product"],
            telemetry["temperature"],
            telemetry["moisture"],
            telemetry["air_pressure"],
            telemetry["vibration"],
            telemetry["timestamp"],
            telemetry["distance_remaining_km"],
            telemetry["spoilage_risk"]
        )
    )

    connection.commit()


    print("Stored Telemetry:")
    print(json.dumps(telemetry, indent=4))
    print("-" * 50)
    