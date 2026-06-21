from io import BytesIO

import boto3
import pandas as pd
import psycopg2

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
# MINIO CLIENT
# =====================

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# =====================
# POSTGRES CONNECTION
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
# HELPER
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

season_lookup_df = pd.read_sql(
    """
    SELECT season_sk, season_year
    FROM dim_season
    """,
    conn,
)

season_lookup = dict(
    zip(
        season_lookup_df["season_year"].astype(int),
        season_lookup_df["season_sk"],
    )
)

venue_lookup_df = pd.read_sql(
    """
    SELECT venue_sk, venue_name
    FROM dim_venue
    """,
    conn,
)

venue_lookup = dict(
    zip(
        venue_lookup_df["venue_name"],
        venue_lookup_df["venue_sk"],
    )
)

# =====================
# READ ALL MATCH FILES
# =====================

response = s3.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix="matches/",
)

match_files = []

for obj in response.get("Contents", []):

    key = obj["Key"]

    if key.endswith(".parquet"):
        match_files.append(key)

print(f"Match Files Found: {len(match_files)}")

all_matches = []

for file_key in sorted(match_files):

    df = read_parquet_from_minio(file_key)

    all_matches.append(df)

matches_df = pd.concat(
    all_matches,
    ignore_index=True,
)

print(f"Matches Read: {len(matches_df)}")

# =====================
# SEASON LOOKUP
# =====================

matches_df["season_sk"] = (
    matches_df["season"]
    .astype(int)
    .map(season_lookup)
)

# =====================
# VENUE NORMALIZATION
# =====================

venue_seed = pd.read_csv(
    "ipl_dbt/seeds/venue_normalization.csv"
)

matches_df = matches_df.merge(
    venue_seed,
    how="left",
    left_on="venue_name",
    right_on="raw_venue",
)

matches_df["canonical_venue_name"] = (
    matches_df["canonical_venue"]
    .fillna(matches_df["venue_name"])
)

# =====================
# VENUE LOOKUP
# =====================

matches_df["venue_sk"] = (
    matches_df["canonical_venue_name"]
    .map(venue_lookup)
)

# =====================
# VALIDATION
# =====================

null_seasons = (
    matches_df["season_sk"]
    .isnull()
    .sum()
)

null_venues = (
    matches_df["venue_sk"]
    .isnull()
    .sum()
)

print("\nUnmatched Venue Names:")

print(
    matches_df[
        matches_df["venue_sk"].isnull()
    ][
        [
            "venue_name",
            "canonical_venue_name"
        ]
    ]
    .drop_duplicates()
    .sort_values("venue_name")
)

print(f"\nNull Season Keys: {null_seasons}")
print(f"Null Venue Keys: {null_venues}")

assert null_seasons == 0
assert null_venues == 0

# =====================
# LOAD DIM_MATCH
# =====================

cursor.execute(
    "TRUNCATE TABLE dim_match RESTART IDENTITY CASCADE"
)

conn.commit()

for _, row in matches_df.iterrows():

    result_margin = row["result_margin"]

    if pd.isna(result_margin):
        result_margin = None
    else:
        result_margin = int(result_margin)

    cursor.execute(
        """
        INSERT INTO dim_match
        (
            match_id,
            season_id,
            match_date,
            venue_id,
            toss_decision,
            result_type,
            result_margin,
            match_type,
            day_or_night
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            str(row["match_id"]),
            int(row["season_sk"]),
            row["match_date"],
            int(row["venue_sk"]),
            row["toss_decision"],
            row["result_type"],
            result_margin,
            row["match_type"],
            None,
        ),
    )

conn.commit()

# =====================
# FINAL VALIDATION
# =====================

cursor.execute(
    "SELECT COUNT(*) FROM dim_match"
)

count = cursor.fetchone()[0]

print(f"\ndim_match Rows: {count}")

cursor.close()
conn.close()

print("Match Load Complete")
