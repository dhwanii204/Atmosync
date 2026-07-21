import random
from datetime import datetime
import time
import random
from datetime import datetime
import time
containers = [
    {"container_id": "C001", "product": "Avocado"},
    {"container_id": "C002", "product": "Mango"},
    {"container_id": "C003", "product": "Banana"},
    {"container_id": "C004", "product": "Orange"},
    {"container_id": "C005", "product": "Grapes"}
]

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


    print(telemetry)

    time.sleep(2)