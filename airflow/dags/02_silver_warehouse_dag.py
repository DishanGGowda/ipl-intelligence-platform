from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"

with DAG(
    dag_id="ipl_silver_warehouse",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ipl", "silver", "warehouse"],
) as dag:

    load_dimensions = BashOperator(
        task_id="load_dimensions",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/07_load_dimensions_to_postgres.py
        """,
    )

    load_matches = BashOperator(
        task_id="load_matches",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/08_load_matches_to_postgres.py
        """,
    )

    load_deliveries = BashOperator(
        task_id="load_deliveries",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/09_load_deliveries_to_postgres.py
        """,
    )

    load_player_innings = BashOperator(
        task_id="load_player_innings",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/10_load_player_innings_to_postgres.py
        """,
    )

    load_player_matchups = BashOperator(
        task_id="load_player_matchups",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/11_load_player_matchups_to_postgres.py
        """,
    )

    load_bowling_spells = BashOperator(
        task_id="load_bowling_spells",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/12_load_bowling_spells_to_postgres.py
        """,
    )

    load_partnerships = BashOperator(
        task_id="load_partnerships",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/warehouse/13_load_partnerships_to_postgres.py
        """,
    )

    (
        load_dimensions
        >> load_matches
        >> load_deliveries
        >> load_player_innings
        >> load_player_matchups
        >> load_bowling_spells
        >> load_partnerships
    )