from pathlib import Path
import tempfile

import yaml
import pandas as pd
import boto3

# =====================
# CONFIG
# =====================

DATASET_PATH = Path("data/cricsheet")

TEAM_SEED_PATH = Path(
    "ipl_dbt/seeds/team_name_normalization.csv"
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
# EXTRACT TEAMS
# =====================

teams = []

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    match_teams = match["info"]["teams"]

    for team in match_teams:

        teams.append(
            {
                "team_name": team
            }
        )

print("Finished extracting teams")

# =====================
# DATAFRAME
# =====================

team_df = pd.DataFrame(teams)

team_df = team_df.drop_duplicates()

print(f"Unique Team Names: {len(team_df)}")

# =====================
# LOAD NORMALIZATION
# =====================

seed_df = pd.read_csv(TEAM_SEED_PATH)

print(f"Normalization Rows: {len(seed_df)}")

team_df = team_df.merge(
    seed_df,
    how="left",
    left_on="team_name",
    right_on="original_name",
)

team_df["canonical_team_name"] = (
    team_df["canonical_name"]
    .fillna(team_df["team_name"])
)

# =====================
# COLLAPSE ALIASES
# =====================

team_df = (
    team_df[
        [
            "canonical_team_name"
        ]
    ]
    .drop_duplicates(
        subset=["canonical_team_name"]
    )
    .sort_values("canonical_team_name")
    .reset_index(drop=True)
)

team_df.insert(
    0,
    "team_id",
    range(1, len(team_df) + 1),
)

print(f"Canonical Team Count: {len(team_df)}")

# =====================
# DATA QUALITY
# =====================

null_names = (
    team_df["canonical_team_name"]
    .isnull()
    .sum()
)

duplicate_names = (
    team_df["canonical_team_name"]
    .duplicated()
    .sum()
)

print(f"Null Team Names: {null_names}")
print(f"Duplicate Canonical Teams: {duplicate_names}")

assert null_names == 0
assert duplicate_names == 0

# =====================
# WRITE PARQUET
# =====================

file_name = "team_master.parquet"

with tempfile.NamedTemporaryFile(
    suffix=".parquet",
    delete=False
) as tmp:

    team_df.to_parquet(
        tmp.name,
        index=False,
        engine="pyarrow"
    )

    s3.upload_file(
        tmp.name,
        BUCKET_NAME,
        f"teams/{file_name}"
    )

print("Team Master Uploaded")
print(f"Final Teams: {len(team_df)}")