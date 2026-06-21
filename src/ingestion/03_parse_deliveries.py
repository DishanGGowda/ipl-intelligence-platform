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
# PARSE DELIVERIES
# =====================

records = []

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    match_id = file.stem
    season = str(match["info"]["dates"][0])[:4]

    innings_list = match["innings"]

    for innings_number, innings in enumerate(innings_list, start=1):

        innings_name = list(innings.keys())[0]
        innings_data = innings[innings_name]

        batting_team = innings_data["team"]

        for delivery in innings_data["deliveries"]:

            ball_key = list(delivery.keys())[0]
            ball_data = delivery[ball_key]

            ball_float = float(ball_key)

            over_number = int(ball_float)
            ball_number = int(round((ball_float - over_number) * 10))

            # =====================
            # EXTRAS
            # =====================

            extras_type = None

            if "extras" in ball_data:
                extras_type = ",".join(ball_data["extras"].keys())

            # =====================
            # WICKETS
            # =====================

            wicket_type = None
            player_dismissed = None
            fielder = None

            if "wicket" in ball_data:

                wicket = ball_data["wicket"]

                wicket_type = wicket.get("kind")
                player_dismissed = wicket.get("player_out")

                fielders = wicket.get("fielders", [])

                if fielders:

                    first_fielder = fielders[0]

                    if isinstance(first_fielder, dict):
                        fielder = first_fielder.get("name")
                    else:
                        fielder = str(first_fielder)

            records.append(
                {
                    "match_id": match_id,
                    "season": season,
                    "innings": innings_number,
                    "batting_team": batting_team,
                    "over_number": over_number,
                    "ball_number": ball_number,
                    "batsman": ball_data.get("batsman"),
                    "non_striker": ball_data.get("non_striker"),
                    "bowler": ball_data.get("bowler"),
                    "runs_batsman": ball_data["runs"]["batsman"],
                    "runs_extras": ball_data["runs"]["extras"],
                    "runs_total": ball_data["runs"]["total"],
                    "extras_type": extras_type,
                    "wicket_type": wicket_type,
                    "player_dismissed": player_dismissed,
                    "fielder": fielder,
                }
            )

print("Finished parsing deliveries")

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
assert df["batsman"].isnull().sum() == 0
assert df["bowler"].isnull().sum() == 0

duplicates = df.duplicated(
    subset=[
        "match_id",
        "innings",
        "over_number",
        "ball_number"
    ]
).sum()

print(f"Duplicate Deliveries: {duplicates}")

# =====================
# WRITE + UPLOAD
# =====================

seasons = sorted(df["season"].unique())

for season in seasons:

    season_df = df[df["season"] == season]

    file_name = f"deliveries_{season}.parquet"

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
            f"deliveries/season={season}/{file_name}"
        )

    print(
        f"Uploaded season {season} "
        f"({len(season_df)} deliveries)"
    )

print("Silver Deliveries Layer Complete")