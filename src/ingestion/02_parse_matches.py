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
# EXTRACT MATCH DATA
# =====================

records = []

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    info = match["info"]

    teams = info.get("teams", [])

    team1 = teams[0] if len(teams) > 0 else None
    team2 = teams[1] if len(teams) > 1 else None

    outcome = info.get("outcome", {})

    winner = outcome.get("winner")

    result_type = None
    result_margin = None

    if "by" in outcome:

        by = outcome["by"]

        if "runs" in by:
            result_type = "runs"
            result_margin = by["runs"]

        elif "wickets" in by:
            result_type = "wickets"
            result_margin = by["wickets"]

    player_of_match = None

    pom = info.get("player_of_match", [])

    if pom:
        player_of_match = pom[0]

    records.append(
        {
            "match_id": file.stem,
            "season": str(info["dates"][0])[:4],
            "match_date": str(info["dates"][0]),
            "venue_name": info.get("venue"),
            "city": info.get("city"),
            "team1": team1,
            "team2": team2,
            "toss_winner": info.get("toss", {}).get("winner"),
            "toss_decision": info.get("toss", {}).get("decision"),
            "winner": winner,
            "result_type": result_type,
            "result_margin": result_margin,
            "player_of_match": player_of_match,
            "match_type": info.get("match_type"),
            "gender": info.get("gender"),
            "overs": info.get("overs"),
        }
    )

print("Finished parsing matches")

# =====================
# DATAFRAME
# =====================

df = pd.DataFrame(records)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

# =====================
# DATA QUALITY
# =====================

assert df["match_id"].isnull().sum() == 0
assert df["match_date"].isnull().sum() == 0

duplicates = df["match_id"].duplicated().sum()

print(f"Duplicate Match IDs: {duplicates}")

# =====================
# WRITE + UPLOAD
# =====================

seasons = sorted(df["season"].unique())

for season in seasons:

    season_df = df[df["season"] == season]

    file_name = f"matches_{season}.parquet"

    with tempfile.NamedTemporaryFile(
        suffix=".parquet",
        delete=False
    ) as tmp:

        season_df.to_parquet(
            tmp.name,
            index=False,
            engine="pyarrow"
        )

        s3.upload_file(
            tmp.name,
            BUCKET_NAME,
            f"matches/season={season}/{file_name}"
        )

    print(
        f"Uploaded season {season} "
        f"({len(season_df)} matches)"
    )

print("Silver Matches Layer Complete")