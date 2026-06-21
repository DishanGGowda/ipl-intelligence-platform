SELECT
    delivery_sk,
    match_sk,
    innings_number,
    over_number,
    ball_number,
    batter_sk,
    bowler_sk,
    runs_batter,
    runs_extras,
    runs_total,
    wicket_flag,
    wicket_type,
    created_at

FROM {{ source('warehouse', 'fact_deliveries') }}