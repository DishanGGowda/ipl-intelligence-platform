from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"

with DAG(
    dag_id="ipl_bronze_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ipl", "bronze"],
) as dag:

    ingest_to_bronze = BashOperator(
        task_id="ingest_to_bronze",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/01_ingest_to_bronze.py
        """,
    )

    parse_matches = BashOperator(
        task_id="parse_matches",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/02_parse_matches.py
        """,
    )

    parse_deliveries = BashOperator(
        task_id="parse_deliveries",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/03_parse_deliveries.py
        """,
    )

    player_registry = BashOperator(
        task_id="player_registry",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/04_build_player_registry.py
        """,
    )

    venue_master = BashOperator(
        task_id="venue_master",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/05_build_venue_master.py
        """,
    )

    team_master = BashOperator(
        task_id="team_master",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/06_build_team_master.py
        """,
    )

    (
        ingest_to_bronze
        >> parse_matches
        >> parse_deliveries
        >> player_registry
        >> venue_master
        >> team_master
    )