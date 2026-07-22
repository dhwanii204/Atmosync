SELECT
    t.container_id,
    t.product,
    t.temperature,
    t.moisture,
    t.air_pressure,
    t.vibration,
    t.timestamp,
    t.distance_remaining_km,
    t.spoilage_risk,
    p.price_per_kg,
    (p.price_per_kg * 1000) AS estimated_container_value
FROM {{ ref('stg_telemetry') }} t
LEFT JOIN commodity_prices p
ON t.product = p.product;