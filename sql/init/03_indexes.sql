CREATE INDEX idx_match_season
ON dim_match(season_id);

CREATE INDEX idx_fact_deliveries_match
ON fact_deliveries(match_sk);

CREATE INDEX idx_fact_deliveries_batter
ON fact_deliveries(batter_sk);

CREATE INDEX idx_fact_deliveries_bowler
ON fact_deliveries(bowler_sk);

CREATE INDEX idx_fact_player_innings_match
ON fact_player_innings(match_sk);

CREATE INDEX idx_fact_player_innings_player
ON fact_player_innings(player_sk);

CREATE INDEX idx_fact_bowling_match
ON fact_bowling_spells(match_sk);

CREATE INDEX idx_fact_bowling_player
ON fact_bowling_spells(bowler_sk);

CREATE INDEX idx_fact_partnership_match
ON fact_partnerships(match_sk);

CREATE INDEX idx_matchups_batter
ON fact_player_matchups(batter_sk);

CREATE INDEX idx_matchups_bowler
ON fact_player_matchups(bowler_sk);