import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

# =====================
# POSTGRES CONFIG
# =====================

POSTGRES_HOST = "ipl-postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "ipl_warehouse"
POSTGRES_USER = "ipl_admin"
POSTGRES_PASSWORD = "ipl_password_2026"

# =====================
# CONNECTION
# =====================

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)

cursor = conn.cursor()

# =====================
# READ INTERMEDIATE TABLE
# =====================

print("Reading int_player_matchups...")

matchups_df = pd.read_sql(
    """
    SELECT
        batter_sk,
        bowler_sk,
        runs,
        balls,
        dismissals
    FROM int_player_matchups
    """,
    conn,
)

print(f"Rows Found: {len(matchups_df)}")

# =====================
# TRUNCATE TARGET
# =====================

print("Clearing fact_player_matchups...")

cursor.execute(
    """
    TRUNCATE TABLE fact_player_matchups
    RESTART IDENTITY
    """
)

conn.commit()

# =====================
# PREPARE RECORDS
# =====================

records = []

for _, row in matchups_df.iterrows():

    records.append(
        (
            int(row["batter_sk"]),
            int(row["bowler_sk"]),
            int(row["runs"]),
            int(row["balls"]),
            int(row["dismissals"]),
        )
    )

print(f"Prepared Records: {len(records)}")

# =====================
# BULK INSERT
# =====================

insert_sql = """
INSERT INTO fact_player_matchups
(
    batter_sk,
    bowler_sk,
    runs_scored,
    balls_faced,
    dismissals
)
VALUES
(
    %s,%s,%s,%s,%s
)
"""

execute_batch(
    cursor,
    insert_sql,
    records,
    page_size=5000,
)

conn.commit()

# =====================
# VALIDATION
# =====================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM fact_player_matchups
    """
)

count = cursor.fetchone()[0]

print(f"fact_player_matchups Rows: {count}")

cursor.close()
conn.close()

print("Player Matchups Load Complete")
