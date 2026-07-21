from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from ingest_crimes import run

def check_row_count(**context):
    result = context['ti'].xcom_pull(task_ids='ingest_crimes_to_s3')
    row_count = result['row_count']
    if row_count == 0:
        raise ValueError(f"Data quality check failed — 0 rows returned")
    if row_count < 1000:
        raise ValueError(f"Data quality check failed — only {row_count} rows, expected at least 1000")
    print(f"Row count check passed — {row_count} rows")

def check_required_columns(**context):
    result = context['ti'].xcom_pull(task_ids='ingest_crimes_to_s3')
    columns = result['columns']
    required = ['id', 'date', 'primary_type', 'district', 'latitude', 'longitude']
    missing = [col for col in required if col not in columns]
    if missing:
        raise ValueError(f"Data quality check failed — missing columns: {missing}")
    print(f"Column check passed — all required columns present")

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

    row_count_check = PythonOperator(
        task_id="check_row_count",
        python_callable=check_row_count,
    )

    column_check = PythonOperator(
        task_id="check_required_columns",
        python_callable=check_required_columns,
    )

    ingest_task >> [row_count_check, column_check]