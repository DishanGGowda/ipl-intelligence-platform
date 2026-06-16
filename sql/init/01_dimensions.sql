CREATE TABLE dim_player (
    player_sk SERIAL PRIMARY KEY,

    player_id VARCHAR(12) NOT NULL,

    player_name VARCHAR(100) NOT NULL,

    player_name_short VARCHAR(20),

    nationality VARCHAR(60),

    batting_style VARCHAR(30),

    bowling_style VARCHAR(60),

    primary_role VARCHAR(20),

    ipl_debut_season SMALLINT,

    effective_date DATE NOT NULL,

    expiry_date DATE,

    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (player_id, effective_date)
);

CREATE TABLE dim_team (
    team_sk SERIAL PRIMARY KEY,

    team_id VARCHAR(50) UNIQUE NOT NULL,

    team_name_current VARCHAR(100) NOT NULL,

    team_city VARCHAR(80),

    active_from_season SMALLINT,

    active_to_season SMALLINT,

    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_venue (
    venue_sk SERIAL PRIMARY KEY,

    venue_id VARCHAR(80) UNIQUE NOT NULL,

    venue_name VARCHAR(150) NOT NULL,

    city VARCHAR(80),

    country VARCHAR(80) DEFAULT 'India',

    capacity INT,

    pitch_type VARCHAR(30),

    first_ipl_season SMALLINT
);

CREATE TABLE dim_season (
    season_sk SERIAL PRIMARY KEY,

    season_year SMALLINT UNIQUE NOT NULL,

    season_name VARCHAR(20),

    num_teams SMALLINT,

    num_matches SMALLINT,

    host_country VARCHAR(80),

    start_date DATE,

    end_date DATE
);

CREATE TABLE dim_match (
    match_sk SERIAL PRIMARY KEY,

    match_id VARCHAR(15) UNIQUE NOT NULL,

    season_id INT REFERENCES dim_season(season_sk),

    match_date DATE NOT NULL,

    venue_id INT REFERENCES dim_venue(venue_sk),

    toss_decision VARCHAR(10),

    result_type VARCHAR(15),

    result_margin SMALLINT,

    match_type VARCHAR(20),

    day_or_night VARCHAR(10)
);