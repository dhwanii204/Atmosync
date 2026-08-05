# AtmoSync 

## Overview

AtmoSync is an IoT-driven logistics analytics platform designed to monitor shipment conditions, identify spoilage risks, and provide operational recommendations for perishable goods during transportation.

The platform simulates real-time container telemetry data, processes environmental conditions, calculates spoilage risk metrics, and presents actionable insights through an interactive Apache Superset dashboard.

The goal is to help logistics teams make data-driven decisions by detecting potential spoilage events early and recommending appropriate actions such as monitoring, inspection, or rerouting.

---

## Business Problem

Perishable goods such as fruits and vegetables are highly sensitive to environmental conditions during transportation. Temperature fluctuations, humidity changes, and extended transit times can increase spoilage risk and lead to financial losses.

Traditional logistics monitoring systems often identify issues only after damage has occurred.

AtmoSync addresses this challenge by providing real-time shipment health monitoring and predictive spoilage intelligence.

---

## Solution

AtmoSync creates an end-to-end analytics pipeline:

1. Generate simulated IoT sensor data from shipping containers.
2. Stream telemetry data through Kafka.
3. Store and process shipment data.
4. Transform raw data into business-ready analytics models using dbt.
5. Calculate spoilage risk and operational recommendations.
6. Visualize insights through an Apache Superset control tower dashboard.

---

## System Architecture
IoT Sensor Simulator
|
↓
Apache Kafka
|
↓
Database Storage
|
↓
dbt
(Analytics Transformation)
|
↓
Spoilage Arbitrage Model
|
↓
Apache Superset Dashboard

---

## Tech Stack

### Data Generation
- Python
- IoT Sensor Simulation

### Data Streaming
- Apache Kafka

### Data Transformation
- dbt Core
- SQL

### Data Storage
- PostgreSQL / Snowflake

### Visualization
- Apache Superset

### Development Tools
- Git & GitHub
- Anaconda Environment

---

## Analytics Logic

The analytics layer calculates:

### Spoilage Risk
Evaluates environmental conditions such as:
- Temperature
- Moisture
- Vibration
- Transit duration

### Time-Based Metrics

- Time to Market
- Time to Spoilage
- Spoilage Margin Hours

### Shipment Classification

Shipments are categorized as:

| Status | Meaning |
|---|---|
| SAFE | Shipment can continue normally |
| MONITOR | Requires inspection at the nearest hub |
| AT RISK | Requires rerouting to minimize losses |

### Operational Recommendations

Examples:

- CONTINUE TO DESTINATION
- INSPECT AT NEAREST HUB
- REROUTE TO NEAREST MARKET

---

## Dashboard

The AtmoSync Logistics Control Tower provides:

### KPI Monitoring
- Total Telemetry Records
- Safe Shipments
- Monitor Shipments
- At-Risk Shipments

### Visual Analytics

- Temperature Fluctuation Monitoring
- Shipment Risk Distribution
- Spoilage Risk Distribution
- Container Journey Progress
- Operational Action Summary
- Critical Shipment Watchlist

---

## Project Structure
Atmosync/
│
├── simulator/ # IoT sensor data generator
├── kafka/ # Streaming configuration
├── processor/ # Data processing logic
├── dbt_project/ # Analytics transformation models
├── snowflake/ # Data warehouse configuration
├── superset/ # Dashboard assets
├── docs/ # Documentation
└── README.md

---

## Future Enhancements

- Real-time alert notifications
- Machine learning based spoilage prediction
- Route optimization using weather intelligence
- Automated market rerouting recommendations
- Cloud deployment

---

## Author

Dhwani Shah

