-- AtmoSync PostgreSQL Performance Optimization
-- Index for container-level time-series telemetry queries

CREATE INDEX IF NOT EXISTS idx_telemetry_container_timestamp
ON public.telemetry (container_id, timestamp);