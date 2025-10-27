import os
import boto3
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password123"
BUCKET = "bronze-transactions" # Minio Bucket Name
LOCAL_DIR = "/tmp/minio_downloads"  # use absolute path for Airflow

SNOWFLAKE_USER = "<<YOUR_USERNAME>>"
SNOWFLAKE_PASSWORD = "<<YOUR_PASSWORD>>"
SNOWFLAKE_ACCOUNT = "<<YOUR_ACCOUNT>>" # Get from Snowflake UI (Session Details)
SNOWFLAKE_WAREHOUSE = "Stock_Wh"
SNOWFLAKE_DB = "STOCKS_DB"
SNOWFLAKE_SCHEMA = "BRONZE"

# Minio Connection
def download_from_minio():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY # Get from Minio UI
    )
    objects = s3.list_objects_v2(Bucket=BUCKET).get("Contents", []) # List all objects in the bucket
    local_files = []
    for obj in objects:
        key = obj["Key"]
        local_file = os.path.join(LOCAL_DIR, os.path.basename(key))
        s3.download_file(BUCKET, key, local_file)
        print(f"Downloaded {key} -> {local_file}")
        local_files.append(local_file)
    return local_files

# Snowflake Connection
def load_to_snowflake(**kwargs):
    local_files = kwargs['ti'].xcom_pull(task_ids='download_minio')
    if not local_files:
        print("No files to load.")
        return

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA
    )
    cur = conn.cursor() # Create a cursor object

    for f in local_files: # Upload files to Snowflake stage
        cur.execute(f"PUT file://{f} @%bronze_stock_raw")
        print(f"Uploaded {f} to Snowflake stage")

    cur.execute("""
        COPY INTO bronze_stock_raw
        FROM @%bronze_stock_raw
        FILE_FORMAT = (TYPE=JSON)
    """)
    print("COPY INTO executed")

    cur.close()
    conn.close()

# Airflow DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 9, 9),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "minio_to_snowflake",
    default_args=default_args,
    schedule_interval="*/1 * * * *",  # Run every 1 minute
    catchup=False,
) as dag:
    # Airflow Tasks
    task1 = PythonOperator(
        task_id="download_minio",
        python_callable=download_from_minio,
    )

    task2 = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_to_snowflake,
        provide_context=True,
    )

    task1 >> task2 # Task Dependencies
