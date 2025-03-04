FROM apache/airflow:latest

USER root

# Install OpenJDK 17 (commonly used for Spark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless curl && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable for the Airflow and Spark containers
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
USER airflow
RUN pip install pyspark==3.5.5