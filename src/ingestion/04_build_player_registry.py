from pathlib import Path
import tempfile

import yaml
import pandas as pd
import boto3

# =====================
# CONFIG
# =====================

DATASET_PATH = Path("data/cricsheet")

MINIO_ENDPOINT = "http://ipl-minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "minio_password_2026"

BUCKET_NAME = "ipl-silver"

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
# BUILD PLAYER REGISTRY
# =====================

players = []

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    registry = (
        match.get("info", {})
        .get("registry", {})
        .get("people", {})
    )

    for player_name, player_id in registry.items():

        players.append(
            {
                "player_name": player_name,
                "player_cricsheet_id": player_id,
            }
        )

print("Finished extracting players")

# =====================
# DATAFRAME
# =====================

df = pd.DataFrame(players)

print(f"Raw Rows: {len(df)}")

# Remove exact duplicate rows
df = df.drop_duplicates()

# Keep one row per Cricsheet ID
df = (
    df
    .sort_values("player_name")
    .drop_duplicates(
        subset=["player_cricsheet_id"],
        keep="first"
    )
    .reset_index(drop=True)
)

print(f"Unique Players: {len(df)}")

# =====================
# DATA QUALITY
# =====================

null_ids = df["player_cricsheet_id"].isnull().sum()

duplicate_ids = df["player_cricsheet_id"].duplicated().sum()

print(f"Null IDs: {null_ids}")
print(f"Duplicate IDs: {duplicate_ids}")

assert null_ids == 0, "Null player IDs found"
assert duplicate_ids == 0, "Duplicate player IDs found"

# =====================
# SORT FINAL OUTPUT
# =====================

df = df.sort_values(
    by=["player_name"]
).reset_index(drop=True)

# =====================
# WRITE PARQUET
# =====================

file_name = "player_registry.parquet"

with tempfile.NamedTemporaryFile(
    suffix=".parquet",
    delete=False
) as tmp:

    df.to_parquet(
        tmp.name,
        index=False,
        engine="pyarrow"
    )

    s3.upload_file(
        tmp.name,
        BUCKET_NAME,
        f"players/{file_name}"
    )

print("Player Registry Uploaded")
print(f"Final Player Count: {len(df)}")