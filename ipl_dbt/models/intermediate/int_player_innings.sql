WITH deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

player_innings AS (

    SELECT

        match_sk,

        batter_sk AS player_sk,

        innings_number,

        COUNT(*) AS balls_faced,

        SUM(runs_batter) AS runs_scored,

        SUM(
            CASE
                WHEN runs_batter = 4 THEN 1
                ELSE 0
            END
        ) AS fours,

        SUM(
            CASE
                WHEN runs_batter = 6 THEN 1
                ELSE 0
            END
        ) AS sixes,

        ROUND(
            (
                SUM(runs_batter)::numeric
                /
                NULLIF(COUNT(*), 0)
            ) * 100,
            2
        ) AS strike_rate

    FROM deliveries

    WHERE batter_sk IS NOT NULL

    GROUP BY
        match_sk,
        batter_sk,
        innings_number

)

SELECT *
FROM player_innings