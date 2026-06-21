from pathlib import Path
import tempfile

import yaml
import pandas as pd
import boto3

# =====================
# CONFIG
# =====================

DATASET_PATH = Path("data/cricsheet")

VENUE_SEED_PATH = Path(
    "ipl_dbt/seeds/venue_normalization.csv"
)

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
# EXTRACT VENUES
# =====================

venues = []

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    info = match["info"]

    venues.append(
        {
            "venue_name": info.get("venue"),
            "city": info.get("city"),
        }
    )

print("Finished extracting venues")

# =====================
# DATAFRAME
# =====================

venue_df = pd.DataFrame(venues)

venue_df = venue_df.drop_duplicates()

print(f"Unique Venue Records: {len(venue_df)}")

# =====================
# LOAD NORMALIZATION
# =====================

seed_df = pd.read_csv(VENUE_SEED_PATH)

print(f"Venue Normalization Rows: {len(seed_df)}")

venue_df = venue_df.merge(
    seed_df,
    how="left",
    left_on="venue_name",
    right_on="raw_venue",
)

venue_df["canonical_venue_name"] = (
    venue_df["canonical_venue"]
    .fillna(venue_df["venue_name"])
)

# =====================
# COLLAPSE ALIASES
# =====================

venue_df = (
    venue_df[
        [
            "canonical_venue_name",
            "city",
        ]
    ]
    .drop_duplicates(
        subset=["canonical_venue_name"]
    )
    .sort_values("canonical_venue_name")
    .reset_index(drop=True)
)

venue_df.insert(
    0,
    "venue_id",
    range(1, len(venue_df) + 1),
)

print(f"Canonical Venue Count: {len(venue_df)}")

# =====================
# DATA QUALITY
# =====================

null_names = (
    venue_df["canonical_venue_name"]
    .isnull()
    .sum()
)

duplicate_names = (
    venue_df["canonical_venue_name"]
    .duplicated()
    .sum()
)

print(f"Null Venue Names: {null_names}")
print(f"Duplicate Canonical Venues: {duplicate_names}")

assert null_names == 0
assert duplicate_names == 0

# =====================
# WRITE PARQUET
# =====================

file_name = "venue_master.parquet"

with tempfile.NamedTemporaryFile(
    suffix=".parquet",
    delete=False
) as tmp:

    venue_df.to_parquet(
        tmp.name,
        index=False,
        engine="pyarrow"
    )

    s3.upload_file(
        tmp.name,
        BUCKET_NAME,
        f"venues/{file_name}"
    )

print("Venue Master Uploaded")
print(f"Final Venues: {len(venue_df)}")