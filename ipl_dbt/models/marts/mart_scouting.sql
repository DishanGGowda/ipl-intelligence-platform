WITH player_stats AS (

    SELECT

        player_name,
        innings_played,
        career_runs,
        strike_rate,
        highest_score,

        CASE
            WHEN strike_rate >= 140
                 AND career_runs >= 1000
            THEN 'Power Hitter'

            WHEN strike_rate >= 120
                 AND career_runs >= 1500
            THEN 'Top Order Batter'

            ELSE 'Developing Player'
        END AS scouting_category

    FROM {{ ref('mart_player_career') }}

)

SELECT *
FROM player_stats