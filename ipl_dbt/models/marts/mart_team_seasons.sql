WITH matches AS (

    SELECT *
    FROM {{ source('warehouse', 'dim_match') }}

),

seasons AS (

    SELECT *
    FROM {{ source('warehouse', 'dim_season') }}

),

deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

team_runs AS (

    SELECT

        m.season_id,

        d.match_sk,

        SUM(d.runs_total) AS team_runs

    FROM deliveries d

    INNER JOIN matches m
        ON d.match_sk = m.match_sk

    GROUP BY
        m.season_id,
        d.match_sk

),

season_summary AS (

    SELECT

        season_id,

        COUNT(DISTINCT match_sk) AS matches_played,

        SUM(team_runs) AS total_runs,

        ROUND(
            AVG(team_runs),
            2
        ) AS avg_runs_per_match

    FROM team_runs

    GROUP BY season_id

)

SELECT

    s.season_year,

    ss.matches_played,
    ss.total_runs,
    ss.avg_runs_per_match

FROM season_summary ss

INNER JOIN seasons s
    ON ss.season_id = s.season_sk 