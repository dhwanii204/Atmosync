
import os
import requests
import psycopg2
from dotenv import load_dotenv
from pathlib import Path


# -----------------------------
# Load environment variables
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)


# -----------------------------
# Database configuration
# -----------------------------

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "atmosync",
    "user": "postgres",
    "password": os.getenv("POSTGRES_PASSWORD"),
}


# -----------------------------
# Slack alert function
# -----------------------------

def send_slack_alert(message):

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("Slack webhook URL not found.")
        return False

    response = requests.post(
        webhook_url,
        json={"text": message},
        timeout=10
    )

    if response.status_code == 200:
        print("Slack alert sent successfully.")
        return True

    print(
        f"Slack alert failed: "
        f"{response.status_code} - {response.text}"
    )

    return False


# -----------------------------
# Database connection
# -----------------------------

def get_database_connection():

    return psycopg2.connect(**DB_CONFIG)


# -----------------------------
# Get latest shipment status
# for every container
# -----------------------------

def get_latest_shipments(connection):

    query = """
    SELECT
        container_id,
        product,
        temperature,
        spoilage_risk,
        distance_remaining_km,
        spoilage_margin_hours,
        shipment_status,
        recommendation
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY container_id
                ORDER BY timestamp DESC
            ) AS row_num
        FROM public.spoilage_arbitrage
    ) AS latest_shipments
    WHERE row_num = 1
    ORDER BY container_id;
    """

    with connection.cursor() as cursor:

        cursor.execute(query)

        return cursor.fetchall()


# -----------------------------
# Check for an active alert
# -----------------------------

def get_active_alert(connection, container_id):

    query = """
    SELECT
        id,
        spoilage_margin_hours,
        recommendation
    FROM alert_log
    WHERE container_id = %s
      AND resolved_at IS NULL
    ORDER BY alerted_at DESC
    LIMIT 1;
    """

    with connection.cursor() as cursor:

        cursor.execute(
            query,
            (container_id,)
        )

        return cursor.fetchone()


# -----------------------------
# Create a new alert record
# -----------------------------

def log_alert(connection, shipment):

    query = """
    INSERT INTO alert_log (
        container_id,
        shipment_status,
        spoilage_margin_hours,
        recommendation
    )
    VALUES (%s, %s, %s, %s);
    """

    with connection.cursor() as cursor:

        cursor.execute(
            query,
            (
                shipment[0],
                shipment[6],
                shipment[5],
                shipment[7],
            )
        )

    connection.commit()


# -----------------------------
# Resolve an active alert
# -----------------------------

def resolve_alert(connection, alert_id):

    query = """
    UPDATE alert_log
    SET resolved_at = CURRENT_TIMESTAMP
    WHERE id = %s;
    """

    with connection.cursor() as cursor:

        cursor.execute(
            query,
            (alert_id,)
        )

    connection.commit()


# -----------------------------
# Main alert-monitor process
# -----------------------------

if __name__ == "__main__":

    connection = None

    try:

        connection = get_database_connection()

        print(
            "Connected to AtmoSync PostgreSQL "
            "database successfully."
        )

        shipments = get_latest_shipments(connection)

        print(
            f"\nLatest shipment records found: "
            f"{len(shipments)}"
        )

        for shipment in shipments:

            (
                container_id,
                product,
                temperature,
                spoilage_risk,
                distance_remaining_km,
                spoilage_margin_hours,
                shipment_status,
                recommendation
            ) = shipment

            print(
                container_id,
                product,
                temperature,
                spoilage_risk,
                distance_remaining_km,
                spoilage_margin_hours,
                shipment_status,
                recommendation
            )

            active_alert = get_active_alert(
                connection,
                container_id
            )

            # -----------------------------
            # Case 1: Container is AT RISK
            # -----------------------------

            if shipment_status == "AT RISK":

                # No active alert exists
                if active_alert is None:

                    message = f"""
🚨 *AT RISK SHIPMENT*

*Container:* {container_id}
*Product:* {product}
*Temperature:* {temperature}°C
*Spoilage Risk:* {spoilage_risk}
*Distance Remaining:* {distance_remaining_km} km
*Spoilage Margin:* {spoilage_margin_hours} hours

*Recommended Action:*
{recommendation}
"""

                    alert_sent = send_slack_alert(message)

                    if alert_sent:

                        log_alert(
                            connection,
                            shipment
                        )

                        print(
                            f"Alert logged for "
                            f"{container_id}."
                        )

                # Active alert already exists
                else:

                    alert_id = active_alert[0]
                    previous_margin = active_alert[1]
                    previous_recommendation = active_alert[2]

                    if (
                        previous_margin
                        == spoilage_margin_hours
                        and
                        previous_recommendation
                        == recommendation
                    ):

                        print(
                            f"Alert already active for "
                            f"{container_id}. "
                            "Skipping Slack notification."
                        )

                    else:

                        message = f"""
⚠️ *AT RISK CONDITION UPDATED*

*Container:* {container_id}
*Product:* {product}
*Temperature:* {temperature}°C
*Spoilage Risk:* {spoilage_risk}
*Distance Remaining:* {distance_remaining_km} km
*Spoilage Margin:* {spoilage_margin_hours} hours

*Updated Recommended Action:*
{recommendation}
"""

                        alert_sent = send_slack_alert(
                            message
                        )

                        if alert_sent:

                            # Resolve previous alert
                            resolve_alert(
                                connection,
                                alert_id
                            )

                            # Log the new alert
                            log_alert(
                                connection,
                                shipment
                            )

                            print(
                                f"Updated alert logged "
                                f"for {container_id}."
                            )

            # -----------------------------
            # Case 2: Container is no longer
            # AT RISK
            # -----------------------------

            else:

                if active_alert is not None:

                    alert_id = active_alert[0]

                    resolve_alert(
                        connection,
                        alert_id
                    )

                    print(
                        f"Alert resolved for "
                        f"{container_id}. "
                        f"Current status: "
                        f"{shipment_status}"
                    )

    except Exception as error:

        print(
            f"Alert monitor failed: {error}"
        )

    finally:

        if connection is not None:

            connection.close()

            print(
                "\nDatabase connection closed."
            )


