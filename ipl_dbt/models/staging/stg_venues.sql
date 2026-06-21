SELECT
    venue_sk,
    venue_id,
    venue_name,
    city,
    country,
    capacity,
    pitch_type,
    first_ipl_season

FROM {{ source('warehouse', 'dim_venue') }}