SELECT
    match_sk,
    match_id,
    season_id,
    match_date,
    venue_id,
    toss_decision,
    result_type,
    result_margin,
    match_type,
    day_or_night

FROM {{ source('warehouse', 'dim_match') }}