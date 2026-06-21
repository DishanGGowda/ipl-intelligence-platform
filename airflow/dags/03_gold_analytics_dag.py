from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project/ipl_dbt"
PROFILES_DIR = "/opt/airflow/project/airflow/dbt"

with DAG(
    dag_id="ipl_gold_analytics",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ipl", "gold", "analytics"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        dbt run --profiles-dir {PROFILES_DIR}
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        dbt test --profiles-dir {PROFILES_DIR}
        """,
    )

    dbt_run >> dbt_test