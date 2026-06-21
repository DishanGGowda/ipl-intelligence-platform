WITH innings AS (

    SELECT *
    FROM {{ ref('int_player_innings') }}

),

players AS (

    SELECT *
    FROM {{ ref('stg_players') }}

),

career AS (

    SELECT

        player_sk,

        COUNT(*) AS innings_played,

        SUM(runs_scored) AS career_runs,

        SUM(balls_faced) AS career_balls,

        SUM(fours) AS career_fours,

        SUM(sixes) AS career_sixes,

        ROUND(
            (
                SUM(runs_scored)::numeric
                /
                NULLIF(SUM(balls_faced),0)
            ) * 100,
            2
        ) AS strike_rate,

        MAX(runs_scored) AS highest_score

    FROM innings

    GROUP BY player_sk

)

SELECT

    p.player_sk,
    p.player_name,
    p.primary_role,
    p.batting_style,
    p.bowling_style,

    c.innings_played,
    c.career_runs,
    c.career_balls,
    c.career_fours,
    c.career_sixes,
    c.strike_rate,
    c.highest_score

FROM career c
JOIN players p
    ON c.player_sk = p.player_sk