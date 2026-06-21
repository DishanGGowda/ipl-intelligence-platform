from io import BytesIO

import boto3
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

# =====================
# MINIO CONFIG
# =====================

MINIO_ENDPOINT = "http://ipl-minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "minio_password_2026"

BUCKET_NAME = "ipl-silver"

# =====================
# POSTGRES CONFIG
# =====================

POSTGRES_HOST = "ipl-postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "ipl_warehouse"
POSTGRES_USER = "ipl_admin"
POSTGRES_PASSWORD = "ipl_password_2026"

# =====================
# CONNECTIONS
# =====================

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)

cursor = conn.cursor()

# =====================
# HELPERS
# =====================

def read_parquet_from_minio(object_key):

    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
    )

    return pd.read_parquet(
        BytesIO(obj["Body"].read())
    )

# =====================
# LOOKUPS
# =====================

print("Loading dimension lookups...")

match_df = pd.read_sql(
    """
    SELECT match_sk, match_id
    FROM dim_match
    """,
    conn,
)

player_df = pd.read_sql(
    """
    SELECT player_sk, player_name
    FROM dim_player
    WHERE is_current = TRUE
    """,
    conn,
)

match_lookup = dict(
    zip(
        match_df["match_id"].astype(str),
        match_df["match_sk"],
    )
)

player_lookup = dict(
    zip(
        player_df["player_name"],
        player_df["player_sk"],
    )
)

print(f"Match Lookup Rows: {len(match_lookup)}")
print(f"Player Lookup Rows: {len(player_lookup)}")

# =====================
# READ DELIVERY FILES
# =====================

response = s3.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix="deliveries/",
)

delivery_files = []

for obj in response.get("Contents", []):

    key = obj["Key"]

    if key.endswith(".parquet"):
        delivery_files.append(key)

print(f"Delivery Files Found: {len(delivery_files)}")

all_deliveries = []

for file_key in sorted(delivery_files):

    df = read_parquet_from_minio(file_key)

    all_deliveries.append(df)

deliveries_df = pd.concat(
    all_deliveries,
    ignore_index=True,
)

print(f"Deliveries Read: {len(deliveries_df)}")

# =====================
# LOOKUPS
# =====================

deliveries_df["match_sk"] = (
    deliveries_df["match_id"]
    .astype(str)
    .map(match_lookup)
)

deliveries_df["batter_sk"] = (
    deliveries_df["batsman"]
    .map(player_lookup)
)

deliveries_df["bowler_sk"] = (
    deliveries_df["bowler"]
    .map(player_lookup)
)

# =====================
# VALIDATION
# =====================

null_match_keys = (
    deliveries_df["match_sk"]
    .isnull()
    .sum()
)

null_batter_keys = (
    deliveries_df["batter_sk"]
    .isnull()
    .sum()
)

null_bowler_keys = (
    deliveries_df["bowler_sk"]
    .isnull()
    .sum()
)

print(f"Null Match Keys: {null_match_keys}")
print(f"Null Batter Keys: {null_batter_keys}")
print(f"Null Bowler Keys: {null_bowler_keys}")

assert null_match_keys == 0

# =====================
# WICKET FLAG
# =====================

deliveries_df["wicket_flag"] = (
    deliveries_df["wicket_type"]
    .notna()
)

# =====================
# TRUNCATE FACT
# =====================

print("Clearing fact_deliveries...")

cursor.execute(
    "TRUNCATE TABLE fact_deliveries RESTART IDENTITY CASCADE"
)

conn.commit()

# =====================
# PREPARE INSERTS
# =====================

records = []

for _, row in deliveries_df.iterrows():

    records.append(
        (
            int(row["match_sk"]),
            int(row["innings"]),
            int(row["over_number"]),
            int(row["ball_number"]),
            (
                int(row["batter_sk"])
                if pd.notna(row["batter_sk"])
                else None
            ),
            (
                int(row["bowler_sk"])
                if pd.notna(row["bowler_sk"])
                else None
            ),
            int(row["runs_batsman"]),
            int(row["runs_extras"]),
            int(row["runs_total"]),
            bool(row["wicket_flag"]),
            row["wicket_type"],
        )
    )

print(f"Prepared Records: {len(records)}")

# =====================
# BULK INSERT
# =====================

print("Loading fact_deliveries...")

insert_sql = """
INSERT INTO fact_deliveries
(
    match_sk,
    innings_number,
    over_number,
    ball_number,
    batter_sk,
    bowler_sk,
    runs_batter,
    runs_extras,
    runs_total,
    wicket_flag,
    wicket_type
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
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
    "SELECT COUNT(*) FROM fact_deliveries"
)

count = cursor.fetchone()[0]

print(f"fact_deliveries Rows: {count}")

cursor.close()
conn.close()

print("Delivery Load Complete")
