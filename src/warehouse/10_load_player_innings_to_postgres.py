import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

POSTGRES_HOST = "ipl-postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "ipl_warehouse"
POSTGRES_USER = "ipl_admin"
POSTGRES_PASSWORD = "ipl_password_2026"

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)

cursor = conn.cursor()

print("Reading int_player_innings...")

innings_df = pd.read_sql(
    """
    SELECT
        match_sk,
        player_sk,
        balls_faced,
        runs_scored,
        fours,
        sixes,
        strike_rate
    FROM int_player_innings
    """,
    conn,
)

print(f"Rows Found: {len(innings_df)}")

print("Clearing fact_player_innings...")

cursor.execute(
    """
    TRUNCATE TABLE fact_player_innings
    RESTART IDENTITY
    """
)

conn.commit()

records = []

for _, row in innings_df.iterrows():

    records.append(
        (
            int(row["match_sk"]),
            int(row["player_sk"]),
            int(row["runs_scored"]),
            int(row["balls_faced"]),
            int(row["fours"]),
            int(row["sixes"]),
            float(row["strike_rate"]),
            None
        )
    )

print(f"Prepared Records: {len(records)}")

insert_sql = """
INSERT INTO fact_player_innings
(
    match_sk,
    player_sk,
    runs_scored,
    balls_faced,
    fours,
    sixes,
    strike_rate,
    dismissal_type
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s,%s
)
"""

execute_batch(
    cursor,
    insert_sql,
    records,
    page_size=5000
)

conn.commit()

cursor.execute(
    """
    SELECT COUNT(*)
    FROM fact_player_innings
    """
)

count = cursor.fetchone()[0]

print(f"fact_player_innings Rows: {count}")

cursor.close()
conn.close()

print("Player Innings Load Complete")
