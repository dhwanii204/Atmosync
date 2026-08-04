WITH base AS (

    SELECT

        id,
        container_id,
        product,
        temperature,
        moisture,
        air_pressure,
        vibration,
        timestamp,
        distance_remaining_km,
        spoilage_risk,

        -- Estimated travel time assuming 50 km/hour
        ROUND(distance_remaining_km / 50.0, 2) AS time_to_market_hours,


        -- Estimated shelf life based on product + temperature
        CASE

            WHEN product = 'Avocado' THEN
                CASE
                    WHEN temperature > 7 THEN 4
                    WHEN temperature > 5 THEN 6
                    ELSE 8
                END

            WHEN product = 'Mango' THEN
                CASE
                    WHEN temperature > 7 THEN 8
                    WHEN temperature > 5 THEN 10
                    ELSE 12
                END

            WHEN product = 'Banana' THEN
                CASE
                    WHEN temperature > 7 THEN 6
                    WHEN temperature > 5 THEN 8
                    ELSE 10
                END

            WHEN product = 'Orange' THEN
                CASE
                    WHEN temperature > 7 THEN 16
                    WHEN temperature > 5 THEN 18
                    ELSE 20
                END

            WHEN product = 'Grapes' THEN
                CASE
                    WHEN temperature > 7 THEN 10
                    WHEN temperature > 5 THEN 12
                    ELSE 14
                END

            ELSE 8

        END AS time_to_spoilage_hours


    FROM telemetry

),


analysis AS (

    SELECT

        *,
        
        ROUND(
            time_to_spoilage_hours - time_to_market_hours,
            2
        ) AS spoilage_margin_hours


    FROM base

)


SELECT

    id,
    container_id,
    product,
    temperature,
    moisture,
    air_pressure,
    vibration,
    timestamp,
    distance_remaining_km,
    spoilage_risk,

    time_to_market_hours,
    time_to_spoilage_hours,
    spoilage_margin_hours,


    CASE

        WHEN spoilage_margin_hours < 0
            THEN 'AT RISK'

        WHEN spoilage_margin_hours <= 2
            THEN 'MONITOR'

        ELSE 'SAFE'

    END AS shipment_status,


    CASE

        WHEN spoilage_margin_hours < 0
            THEN 'REROUTE TO NEAREST MARKET'

        WHEN spoilage_margin_hours <= 2
            THEN 'INSPECT AT NEAREST HUB'

        ELSE 'CONTINUE TO DESTINATION'

    END AS recommendation


FROM analysis