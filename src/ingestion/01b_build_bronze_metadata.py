from pathlib import Path
from datetime import datetime, UTC
import json

import yaml
import boto3

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

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# =====================
# BUILD METADATA
# =====================

manifest = []
schema_versions = {}

files = list(DATASET_PATH.glob("*.yaml"))

print(f"Found {len(files)} YAML files")

for idx, file in enumerate(files, start=1):

    if idx % 100 == 0:
        print(f"Processed {idx} files")

    with open(file, "r", encoding="utf-8") as f:
        match = yaml.safe_load(f)

    match_id = file.stem

    year = str(match["info"]["dates"][0])[:4]

    version = str(match["meta"]["data_version"])

    manifest.append(
        {
            "match_id": match_id,
            "filename": file.name,
            "year": int(year),
            "schema_version": version,
            "ingested_at": datetime.now(UTC).isoformat(),
        }
    )

    schema_versions[match_id] = version

print("Finished parsing YAML files")

# =====================
# SAVE LOCAL FILES
# =====================

manifest_file = Path("ingestion_manifest.json")
schema_file = Path("schema_versions.json")

with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

with open(schema_file, "w", encoding="utf-8") as f:
    json.dump(schema_versions, f, indent=2)

print("Metadata files created")

# =====================
# UPLOAD TO MINIO
# =====================

print("Uploading manifest...")

s3.upload_file(
    str(manifest_file),
    BUCKET_NAME,
    "_metadata/ingestion_manifest.json",
)

print("Uploading schema versions...")

s3.upload_file(
    str(schema_file),
    BUCKET_NAME,
    "_metadata/schema_versions.json",
)

print(f"Manifest records: {len(manifest)}")
print(f"Schema records: {len(schema_versions)}")
print("Metadata uploaded successfully")