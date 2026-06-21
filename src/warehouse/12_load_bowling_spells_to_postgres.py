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

print("Reading int_bowling_spells...")

bowling_df = pd.read_sql(
    """
    SELECT
        match_sk,
        bowler_sk,
        overs_bowled,
        runs_conceded,
        wickets,
        economy_rate
    FROM int_bowling_spells
    """,
    conn,
)

print(f"Rows Found: {len(bowling_df)}")

print("Clearing fact_bowling_spells...")

cursor.execute(
    """
    TRUNCATE TABLE fact_bowling_spells
    RESTART IDENTITY
    """
)

conn.commit()

records = []

for _, row in bowling_df.iterrows():

    records.append(
        (
            int(row["match_sk"]),
            int(row["bowler_sk"]),
            float(row["overs_bowled"]),
            0,
            int(row["runs_conceded"]),
            int(row["wickets"]),
            float(row["economy_rate"]),
        )
    )

print(f"Prepared Records: {len(records)}")

insert_sql = """
INSERT INTO fact_bowling_spells
(
    match_sk,
    bowler_sk,
    overs,
    maidens,
    runs_conceded,
    wickets,
    economy
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s
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
    FROM fact_bowling_spells
    """
)

count = cursor.fetchone()[0]

print(f"fact_bowling_spells Rows: {count}")

cursor.close()
conn.close()

print("Bowling Spells Load Complete")
