# AtmoSync Week 2 Progress

## ELT Pipeline Preparation

### Staging Layer

Created dbt staging model:

`stg_telemetry.sql`

Purpose:
- Clean incoming IoT telemetry data
- Standardize sensor fields
- Prepare data for analytics processing

Fields processed:
- Container ID
- Product
- Temperature
- Moisture
- Air Pressure
- Vibration
- Timestamp
- Distance Remaining

---

## Analytics Layer

Created analytics model:

`shipment_analysis.sql`

Purpose:
- Combine telemetry data with commodity pricing information
- Generate analytics-ready shipment data

Integration:
- Telemetry data
- Commodity price dataset

Output metrics:
- Spoilage risk
- Product price
- Estimated shipment value

---

## Current Pipeline Status

IoT Simulator
        |
        ↓
Kafka Topic (fruit_telemetry)
        |
        ↓
Kafka Consumer
        |
        ↓
Analytics Processing
        |
        ↓
Warehouse Layer (Pending confirmation)
        |
        ↓
dbt Transformation Models
        |
        ↓
Superset Dashboard (Pending warehouse setup)
