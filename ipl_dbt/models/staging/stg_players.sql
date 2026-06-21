SELECT
    player_sk,
    player_id,
    player_name,
    player_name_short,
    nationality,
    batting_style,
    bowling_style,
    primary_role,
    ipl_debut_season,
    effective_date,
    expiry_date,
    is_current,
    created_at

FROM {{ source('warehouse', 'dim_player') }}

WHERE is_current = TRUE