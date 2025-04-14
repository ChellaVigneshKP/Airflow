from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "Rafael Vera-Maranon",
    "start_date": days_ago(1),  # Adjust start date as needed
    "retries": 1,
}

dag = DAG(
    dag_id="spark_wordcount_flow",  # Name of your DAG
    default_args=default_args,
    schedule_interval="@daily",  # You can change this schedule as needed
    catchup=False,
)

# Task to print a simple start message
start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag,
)

# SparkSubmitOperator task to run the Spark job
python_job = SparkSubmitOperator(
    task_id="python_job",
    conn_id="spark_default",  # Ensure you have the connection setup in Airflow UI
    application="/opt/airflow/dags/wordcountjob.py",  # Path to the Spark Python script
    name="arrow-spark",  # Spark job name
    conf={
        "spark.master": "spark://spark-master:7077",  # Pass 'master' as part of the 'conf'
        "spark.network.timeout": "600s",
        "spark.executor.heartbeatInterval": "60s",
        "spark.driver.connectTimeout": "600s",
    },
    verbose=True,  # Enable detailed logging for debugging
    dag=dag,
)

# Task to print a completion message after job finishes
end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag,
)

# Define the task dependencies
start >> python_job >> end