WITH deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

bowling_spells AS (

    SELECT

        match_sk,

        bowler_sk,

        innings_number,

        COUNT(*) AS balls_bowled,

        ROUND(
            COUNT(*)::numeric / 6,
            1
        ) AS overs_bowled,

        SUM(runs_total) AS runs_conceded,

        SUM(
            CASE
                WHEN wicket_flag = TRUE
                THEN 1
                ELSE 0
            END
        ) AS wickets,

        ROUND(
            (
                SUM(runs_total)::numeric
                /
                NULLIF(COUNT(*)::numeric / 6, 0)
            ),
            2
        ) AS economy_rate

    FROM deliveries

    WHERE bowler_sk IS NOT NULL

    GROUP BY
        match_sk,
        bowler_sk,
        innings_number

)

SELECT *
FROM bowling_spells