from pathlib import Path
import yaml
import boto3
from botocore.exceptions import ClientError

# =====================
# CONFIG
# =====================

MINIO_ENDPOINT = "http://ipl-minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "minio_password_2026"

BUCKET_NAME = "ipl-bronze"

DATASET_PATH = Path("data/cricsheet")

# =====================
# MINIO CLIENT
# =====================

MINIO_ENDPOINT = "http://ipl-minio:9000"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# =====================
# ENSURE BUCKET EXISTS
# =====================

try:
    s3.head_bucket(Bucket=BUCKET_NAME)
    print(f"Bucket Exists: {BUCKET_NAME}")

except ClientError:
    print(f"Creating Bucket: {BUCKET_NAME}")

    s3.create_bucket(
        Bucket=BUCKET_NAME
    )

# =====================
# UPLOAD FILES
# =====================

uploaded = 0

yaml_files = list(
    DATASET_PATH.glob("*.yaml")
)

print(
    f"Files Found: {len(yaml_files)}"
)

for file in yaml_files:

    try:

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            match = yaml.safe_load(f)

        year = str(
            match["info"]["dates"][0]
        )[:4]

        object_key = (
            f"cricsheet/matches/year={year}/{file.name}"
        )

        s3.upload_file(
            str(file),
            BUCKET_NAME,
            object_key
        )

        uploaded += 1

        if uploaded % 100 == 0:
            print(
                f"Uploaded {uploaded}"
            )

    except Exception as e:

        print(
            f"Failed: {file.name}"
        )

        print(e)

print()
print(
    f"Total Uploaded: {uploaded}"
)

print(
    "Bronze Ingestion Complete"
)