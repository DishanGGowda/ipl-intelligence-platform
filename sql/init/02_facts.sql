CREATE TABLE fact_deliveries (
    delivery_sk BIGSERIAL PRIMARY KEY,

    match_sk INT NOT NULL REFERENCES dim_match(match_sk),

    innings_number SMALLINT NOT NULL,

    over_number SMALLINT NOT NULL,

    ball_number SMALLINT NOT NULL,

    batter_sk INT REFERENCES dim_player(player_sk),

    bowler_sk INT REFERENCES dim_player(player_sk),

    runs_batter SMALLINT DEFAULT 0,

    runs_extras SMALLINT DEFAULT 0,

    runs_total SMALLINT DEFAULT 0,

    wicket_flag BOOLEAN DEFAULT FALSE,

    wicket_type VARCHAR(30),

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE fact_player_innings (
    innings_sk BIGSERIAL PRIMARY KEY,

    match_sk INT REFERENCES dim_match(match_sk),

    player_sk INT REFERENCES dim_player(player_sk),

    runs_scored INT,

    balls_faced INT,

    fours INT,

    sixes INT,

    strike_rate NUMERIC(6,2),

    dismissal_type VARCHAR(30)
);

CREATE TABLE fact_bowling_spells (
    spell_sk BIGSERIAL PRIMARY KEY,

    match_sk INT REFERENCES dim_match(match_sk),

    bowler_sk INT REFERENCES dim_player(player_sk),

    overs NUMERIC(4,1),

    maidens INT,

    runs_conceded INT,

    wickets INT,

    economy NUMERIC(6,2)
);

CREATE TABLE fact_partnerships (
    partnership_sk BIGSERIAL PRIMARY KEY,

    match_sk INT REFERENCES dim_match(match_sk),

    batter1_sk INT REFERENCES dim_player(player_sk),

    batter2_sk INT REFERENCES dim_player(player_sk),

    runs INT,

    balls INT
);

CREATE TABLE fact_player_matchups (
    matchup_sk BIGSERIAL PRIMARY KEY,

    batter_sk INT REFERENCES dim_player(player_sk),

    bowler_sk INT REFERENCES dim_player(player_sk),

    runs_scored INT,

    balls_faced INT,

    dismissals INT
);

