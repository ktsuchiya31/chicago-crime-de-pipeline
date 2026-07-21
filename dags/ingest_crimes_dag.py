from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from ingest_crimes import run

with DAG(
    dag_id="ingest_crimes",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["chicago", "ingestion"]
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_crimes_to_s3",
        python_callable=run
    )