import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "ipl-postgres",
    "port": 5432,
    "database": "ipl_warehouse",
    "user": "ipl_admin",
    "password": "ipl_password_2026"
}

print("Reading int_partnerships...")

conn = psycopg2.connect(**DB_CONFIG)

partnerships_df = pd.read_sql(
    """
    SELECT
        match_sk,
        batter1_sk,
        batter2_sk,
        runs,
        balls
    FROM int_partnerships
    """,
    conn
)

print(f"Rows Found: {len(partnerships_df)}")

cursor = conn.cursor()

print("Clearing fact_partnerships...")

cursor.execute(
    "TRUNCATE TABLE fact_partnerships RESTART IDENTITY;"
)

records = []

for _, row in partnerships_df.iterrows():

    records.append(
        (
            int(row["match_sk"]),
            int(row["batter1_sk"]),
            None if pd.isna(row["batter2_sk"]) else int(row["batter2_sk"]),
            int(row["runs"]),
            int(row["balls"])
        )
    )

print(f"Prepared Records: {len(records)}")

cursor.executemany(
    """
    INSERT INTO fact_partnerships
    (
        match_sk,
        batter1_sk,
        batter2_sk,
        runs,
        balls
    )
    VALUES (%s,%s,%s,%s,%s)
    """,
    records
)

conn.commit()

cursor.execute(
    "SELECT COUNT(*) FROM fact_partnerships"
)

print(
    f"fact_partnerships Rows: {cursor.fetchone()[0]}"
)

cursor.close()
conn.close()

print("Partnership Load Complete")
