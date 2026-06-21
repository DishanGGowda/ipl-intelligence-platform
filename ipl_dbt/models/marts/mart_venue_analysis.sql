WITH venue_stats AS (

    SELECT

        v.venue_name,
        v.city,

        COUNT(DISTINCT m.match_sk) AS matches_played,

        SUM(fd.runs_total) AS total_runs,

        ROUND(
            SUM(fd.runs_total)::numeric
            /
            COUNT(DISTINCT m.match_sk),
            2
        ) AS avg_runs_per_match

    FROM {{ source('warehouse', 'fact_deliveries') }} fd

    JOIN {{ source('warehouse', 'dim_match') }} m
        ON m.match_sk = fd.match_sk

    JOIN {{ source('warehouse', 'dim_venue') }} v
        ON v.venue_sk = m.venue_id

    GROUP BY
        v.venue_name,
        v.city

)

SELECT *
FROM venue_stats