from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
import logging

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),  # Adjust the start date as per requirement
}

# Define the DAG
dag = DAG(
    dag_id="spark_wordcount_dag",
    default_args=default_args,
    description="A simple DAG to run PySpark job",
    schedule_interval="@daily",  # Run the DAG daily
    catchup=False,  # Do not run past scheduled runs
)

# Task to run PySpark job
spark_submit_task = SparkSubmitOperator(
    task_id="run_pyspark_job", 
    conn_id="spark_default",  # Use the default Spark connection setup
    application="/opt/airflow/dags/wordcountjob.py",  # Path to your PySpark script
    name="spark_wordcount_job",
    conf={'spark.master': 'spark://spark-master:7077'},
    verbose=True,
    dag=dag,
)

# Add logging to monitor task progress
def log_success(context):
    logging.info(f"Task {context['task_instance'].task_id} succeeded!")
    logging.info(f"Log URL: {context['task_instance'].log_url}")

# Add on_success callback for logging
spark_submit_task.on_success_callback = log_success