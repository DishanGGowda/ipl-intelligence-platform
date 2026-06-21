WITH innings AS (

    SELECT
        pi.*,
        m.season_id

    FROM {{ ref('int_player_innings') }} pi

    INNER JOIN {{ ref('stg_matches') }} m
        ON pi.match_sk = m.match_sk

),

season_stats AS (

    SELECT

        player_sk,
        season_id,

        COUNT(*) AS innings_played,

        SUM(runs_scored) AS runs,

        SUM(balls_faced) AS balls,

        SUM(fours) AS fours,

        SUM(sixes) AS sixes,

        MAX(runs_scored) AS highest_score,

        ROUND(
            (
                SUM(runs_scored)::numeric
                /
                NULLIF(SUM(balls_faced),0)
            ) * 100,
            2
        ) AS strike_rate

    FROM innings

    GROUP BY
        player_sk,
        season_id

)

SELECT

    p.player_name,
    s.season_year,

    ss.*

FROM season_stats ss

INNER JOIN {{ ref('stg_players') }} p
    ON ss.player_sk = p.player_sk

INNER JOIN {{ source('warehouse','dim_season') }} s
    ON ss.season_id = s.season_sk