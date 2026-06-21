WITH deliveries AS (

    SELECT *
    FROM {{ ref('stg_deliveries') }}

),

partnerships AS (

    SELECT

        match_sk,

        innings_number,

        batter_sk,

        SUM(runs_total) AS partnership_runs,

        COUNT(*) AS partnership_balls

    FROM deliveries

    WHERE batter_sk IS NOT NULL

    GROUP BY
        match_sk,
        innings_number,
        batter_sk

)

SELECT

    ROW_NUMBER() OVER() AS partnership_id,

    match_sk,

    batter_sk AS batter1_sk,

    NULL AS batter2_sk,

    partnership_runs AS runs,

    partnership_balls AS balls

FROM partnerships