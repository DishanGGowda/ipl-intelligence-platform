WITH deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

phase_mapping AS (

    SELECT

        match_sk,
        batter_sk,
        bowler_sk,
        innings_number,

        CASE
            WHEN over_number <= 5 THEN 'Powerplay'
            WHEN over_number <= 14 THEN 'Middle'
            ELSE 'Death'
        END AS phase,

        runs_batter,
        runs_total,
        wicket_flag

    FROM deliveries

),

aggregated AS (

    SELECT

        phase,

        COUNT(*) AS balls,

        SUM(runs_total) AS runs,

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
        ) AS run_rate

    FROM phase_mapping

    GROUP BY phase

)

SELECT *
FROM aggregated