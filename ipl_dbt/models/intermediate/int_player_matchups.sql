WITH deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

matchups AS (

    SELECT

        batter_sk,

        bowler_sk,

        COUNT(*) AS balls,

        SUM(runs_batter) AS runs,

        SUM(
            CASE
                WHEN wicket_flag = TRUE
                THEN 1
                ELSE 0
            END
        ) AS dismissals,

        ROUND(
            (
                SUM(runs_batter)::numeric
                /
                NULLIF(COUNT(*),0)
            ) * 100,
            2
        ) AS strike_rate

    FROM deliveries

    WHERE batter_sk IS NOT NULL
      AND bowler_sk IS NOT NULL

    GROUP BY
        batter_sk,
        bowler_sk

)

SELECT *
FROM matchups