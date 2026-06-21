from io import BytesIO
from datetime import date

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
# LOAD PLAYERS
# =====================

print("Loading Players...")

players_df = read_parquet_from_minio(
    "players/player_registry.parquet"
)

cursor.execute("TRUNCATE TABLE dim_player RESTART IDENTITY CASCADE")

for _, row in players_df.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_player
        (
            player_id,
            player_name,
            effective_date,
            is_current
        )
        VALUES
        (%s,%s,%s,%s)
        """,
        (
            row["player_cricsheet_id"],
            row["player_name"],
            date.today(),
            True,
        ),
    )

conn.commit()

print(f"Players Loaded: {len(players_df)}")

# =====================
# LOAD TEAMS
# =====================

print("Loading Teams...")

teams_df = read_parquet_from_minio(
    "teams/team_master.parquet"
)

cursor.execute("TRUNCATE TABLE dim_team RESTART IDENTITY CASCADE")

for _, row in teams_df.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_team
        (
            team_id,
            team_name_current,
            is_active
        )
        VALUES
        (%s,%s,%s)
        """,
        (
            row["canonical_team_name"],
            row["canonical_team_name"],
            True,
        ),
    )

conn.commit()

print(f"Teams Loaded: {len(teams_df)}")

# =====================
# LOAD VENUES
# =====================

print("Loading Venues...")

venues_df = read_parquet_from_minio(
    "venues/venue_master.parquet"
)

cursor.execute("TRUNCATE TABLE dim_venue RESTART IDENTITY CASCADE")

for _, row in venues_df.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_venue
        (
            venue_id,
            venue_name,
            city
        )
        VALUES
        (%s,%s,%s)
        """,
        (
            row["canonical_venue_name"],
            row["canonical_venue_name"],
            row["city"],
        ),
    )

conn.commit()

print(f"Venues Loaded: {len(venues_df)}")

# =====================
# BUILD SEASON DIMENSION
# =====================

print("Building Seasons...")

matches_objects = s3.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix="matches/"
)

season_files = []

for obj in matches_objects.get("Contents", []):

    key = obj["Key"]

    if key.endswith(".parquet"):
        season_files.append(key)

season_rows = []

for file_key in season_files:

    df = read_parquet_from_minio(file_key)

    season_year = int(df["season"].iloc[0])

    season_rows.append(
        {
            "season_year": season_year,
            "num_matches": len(df),
            "start_date": pd.to_datetime(
                df["match_date"]
            ).min(),
            "end_date": pd.to_datetime(
                df["match_date"]
            ).max(),
        }
    )

season_df = pd.DataFrame(season_rows)

season_df = (
    season_df
    .sort_values("season_year")
    .drop_duplicates()
)

cursor.execute("TRUNCATE TABLE dim_season RESTART IDENTITY CASCADE")

for _, row in season_df.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_season
        (
            season_year,
            season_name,
            num_matches,
            start_date,
            end_date
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """,
        (
            int(row["season_year"]),
            f"IPL {int(row['season_year'])}",
            int(row["num_matches"]),
            row["start_date"],
            row["end_date"],
        ),
    )

conn.commit()

print(f"Seasons Loaded: {len(season_df)}")

# =====================
# VALIDATION
# =====================

print("\nWarehouse Counts")

for table in [
    "dim_player",
    "dim_team",
    "dim_venue",
    "dim_season",
]:
    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count}")

cursor.close()
conn.close()

print("\nDimension Load Complete")
