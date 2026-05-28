from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
from pipeline_tasks import extract_and_save, transform_and_save, load_to_warehouse

DBT_PROJECT_DIR = "/usr/local/airflow/projects/mvv-pipeline/transformation_dbt"

with DAG(
    dag_id="mvv_pipeline",
    schedule="*/30 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id="extract_and_save",
        python_callable=extract_and_save
    )

    task_transform = PythonOperator(
        task_id="transform_and_save",
        python_callable=transform_and_save
    )

    task_load = PythonOperator(
        task_id="load_to_warehouse",
        python_callable=load_to_warehouse
    )

    task_dbt = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR}"
    )

    task_extract >> task_transform >> task_load >> task_dbt
