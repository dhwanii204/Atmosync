# AtmoSync System Architecture

## Overview

AtmoSync follows an end-to-end analytics architecture that transforms real-time IoT container telemetry into actionable logistics insights.

The pipeline consists of data generation, streaming, processing, analytics transformation, and visualization layers.

---

## Data Flow
IoT Sensor Simulator
|
↓
Apache Kafka
|
↓
Data Storage Layer
|
↓
Analytics Processing
|
↓
dbt Transformation Layer
|
↓
Spoilage Arbitrage Model
|
↓
Apache Superset Dashboard

---

## Components

### 1. IoT Sensor Simulator

A Python-based simulator generates container telemetry including:

- Container ID
- Product type
- Temperature
- Moisture
- Air pressure
- Vibration
- Distance remaining
- Timestamp

---

### 2. Apache Kafka

Kafka acts as the streaming layer responsible for handling continuous telemetry events from containers.

---

### 3. Data Processing Layer

The processor handles incoming telemetry and prepares data for analytics calculations.

---

### 4. dbt Analytics Layer

dbt transforms raw shipment data into business-ready models.

The Spoilage Arbitrage model calculates:

- Spoilage risk
- Time to market
- Time to spoilage
- Spoilage margin hours
- Shipment status
- Operational recommendations

---

### 5. Apache Superset Dashboard

The dashboard provides logistics teams with:

- Shipment health monitoring
- Risk distribution
- Temperature analysis
- Recommended operational actions
- Critical shipment tracking

---

## Business Decision Flow
Sensor Conditions
|
↓
Risk Calculation
|
↓
Shipment Classification
|
↓
Operational Recommendation

Example:

High spoilage risk → Reroute to nearest market

Medium risk → Inspect at nearest hub

Low risk → Continue to destination