# AtmoSync Database Performance Optimization

## Telemetry Query Optimization

The `telemetry` table contains continuously generated IoT shipment data.

A composite B-tree index was added on:

- `container_id`
- `timestamp`

```sql
CREATE INDEX idx_telemetry_container_timestamp
ON public.telemetry (container_id, timestamp);