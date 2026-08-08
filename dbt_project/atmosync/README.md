# AtmoSync

## Overview

AtmoSync is an IoT-driven logistics analytics platform designed to monitor shipment conditions, identify spoilage risks, and provide operational recommendations for perishable goods during transportation.

The platform simulates container telemetry data, processes environmental conditions, calculates shipment risk metrics, and presents actionable insights through an interactive Apache Superset dashboard.

AtmoSync also includes an automated alert-monitoring layer that detects at-risk shipments and sends operational alerts to Slack while preventing duplicate notifications and tracking alert resolution.

The goal is to help logistics teams detect potential spoilage events early and take timely actions such as monitoring, inspection, or rerouting.

---

## Business Problem

Perishable goods such as fruits and vegetables are highly sensitive to environmental conditions during transportation. Temperature fluctuations, moisture changes, vibration, and extended transit times can increase spoilage risk and lead to financial losses.

Traditional logistics monitoring systems may identify shipment problems only after significant damage has occurred.

AtmoSync addresses this challenge by combining IoT telemetry, analytics engineering, business intelligence, and automated alerting to provide a shipment-level logistics control tower.

---

## Solution

AtmoSync provides an end-to-end analytics pipeline:

1. Generate simulated IoT sensor telemetry from shipping containers.
2. Stream telemetry through Apache Kafka.
3. Store shipment telemetry in PostgreSQL.
4. Transform raw telemetry into business-ready analytics models using dbt.
5. Calculate time-to-market, time-to-spoilage, and spoilage-margin metrics.
6. Classify shipments as SAFE, MONITOR, or AT RISK.
7. Generate operational recommendations such as inspection or rerouting.
8. Visualize shipment intelligence through an Apache Superset dashboard.
9. Detect at-risk shipments through an automated Python alert monitor.
10. Send actionable alerts to Slack.
11. Prevent duplicate alerts and track when previously active alerts are resolved.

---

## System Architecture

```text
IoT Sensor Simulator
        |
        ↓
Apache Kafka
        |
        ↓
PostgreSQL
        |
        ↓
dbt Core
        |
        ↓
Spoilage Arbitrage Model
        |
        ├──────────────→ Apache Superset
        |
        ↓
Alert Monitor
        |
        ↓
Slack
```

---

## Tech Stack

### Data Generation

* Python
* IoT Sensor Simulation

### Data Streaming

* Apache Kafka

### Data Storage

* PostgreSQL

### Data Transformation

* dbt Core
* SQL

### Business Intelligence

* Apache Superset

### Alerting

* Python
* Slack Incoming Webhooks

### Development & Version Control

* Git
* GitHub
* Anaconda / Python Environment
* Windows Task Scheduler

---

## Analytics Logic

The analytics layer combines environmental and shipment information to evaluate shipment health.

### Environmental Factors

The analysis considers telemetry variables including:

* Temperature
* Moisture
* Air pressure
* Vibration
* Distance remaining
* Timestamp

### Time-Based Metrics

AtmoSync calculates:

* **Time to Market** — estimated remaining travel time based on distance.
* **Time to Spoilage** — estimated product shelf life based on product type and temperature.
* **Spoilage Margin Hours** — difference between estimated time to spoilage and estimated time to market.

A negative spoilage margin indicates that the shipment is expected to reach spoilage conditions before reaching the market.

### Shipment Classification

Shipments are categorized as:

| Status  | Meaning                                               |
| ------- | ----------------------------------------------------- |
| SAFE    | Shipment can continue normally.                       |
| MONITOR | Shipment requires closer monitoring or inspection.    |
| AT RISK | Shipment requires immediate operational intervention. |

### Operational Recommendations

Depending on shipment status, AtmoSync generates recommendations such as:

* `CONTINUE TO DESTINATION`
* `INSPECT AT NEAREST HUB`
* `REROUTE TO NEAREST MARKET`

---

## Spoilage Arbitrage

The **Spoilage Arbitrage** model combines estimated transit time and estimated product shelf life to identify opportunities for operational intervention.

The core business metric is:

```text
Spoilage Margin
= Time to Spoilage - Time to Market
```

When the spoilage margin becomes negative, the shipment is classified as **AT RISK** and the system recommends rerouting to the nearest suitable market.

This converts raw telemetry into an actionable business decision rather than simply displaying sensor measurements.

---

## Dashboard

The AtmoSync Logistics Control Tower is built using Apache Superset.

### KPI Monitoring

The dashboard provides KPI monitoring for:

* Total Telemetry Records
* Safe Shipments
* Monitor Shipments
* At-Risk Shipments

### Visual Analytics

The dashboard contains:

* **Temperature Fluctuation Monitoring**
* **Shipment Risk Distribution**
* **Spoilage Risk Distribution**
* **Container Journey Progress**
* **Operational Action Summary**
* **Critical Shipment Watchlist**

A dashboard filter allows users to interactively filter the available dashboard visualizations.

---

## Automated Alerting

AtmoSync includes a Python-based alert monitor that checks the latest shipment status for each container.

When a shipment becomes **AT RISK**, the system generates a Slack notification containing:

* Container ID
* Product
* Temperature
* Spoilage risk
* Distance remaining
* Spoilage margin
* Recommended operational action

### Alert Deduplication

The system maintains an `alert_log` table in PostgreSQL.

If the same at-risk condition has already generated an alert, the system skips sending another notification.

This prevents repeated Slack messages for the same unchanged risk condition.

### Alert Resolution

When a container previously marked as AT RISK becomes SAFE or MONITOR, the corresponding alert is marked as resolved using the `resolved_at` timestamp.

If the container becomes AT RISK again later, the system can generate a new alert.

This creates an alert lifecycle:

```text
AT RISK
   ↓
Slack Alert
   ↓
Alert Logged
   ↓
SAFE / MONITOR
   ↓
Alert Resolved
   ↓
New AT RISK
   ↓
New Slack Alert
```

---

## Example Alert

```text
🚨 AT RISK SHIPMENT

Container: C001
Product: Avocado
Temperature: 7.2°C
Spoilage Risk: HIGH
Distance Remaining: 281 km
Spoilage Margin: -1.62 hours

Recommended Action:
REROUTE TO NEAREST MARKET
```

---

## Project Structure

```text
Atmosync/
│
├── simulator/              # IoT sensor data generator
├── kafka/                  # Kafka configuration
├── automation/             # Automated alert monitoring
├── dbt_project/            # dbt analytics transformation
├── snowflake/              # Warehouse-related project assets
├── superset/               # Dashboard assets
├── docs/                   # Project documentation
└── README.md
```

---

## Performance & Engineering Improvements

The project includes engineering refinements to improve analytical performance and usability, including:

* Database indexing for frequently queried shipment data.
* Latest-record selection using window functions.
* Business-ready dbt models instead of relying directly on raw telemetry.
* Dashboard-level filtering for interactive analysis.
* Alert deduplication to prevent notification spam.
* Persistent alert history and resolution tracking.
* Environment variables for sensitive credentials and webhook configuration.

---

## Project Outcome

AtmoSync demonstrates an end-to-end analytics workflow that connects:

**IoT data → streaming → database → analytics engineering → business intelligence → automated operational action.**

Instead of only reporting that a shipment has abnormal environmental conditions, the platform translates those conditions into a business decision:

> **What is happening? → How serious is it? → What should the logistics team do?**

---

## Future Enhancements

Potential future extensions include:

* Machine-learning-based spoilage prediction.
* Weather intelligence integration.
* Automated route optimization.
* Market-demand-aware rerouting.
* Cloud deployment.
* Real production IoT sensor integration.

---

## Author

**Dhwani Shah**

```
```


