import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.python import PythonSensor
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "email_on_failure": True,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
        "02_dag_train_pipeline",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=days_ago(1),
) as dag:
    download = DockerOperator(
        image="airflow-download",
        command="/data/raw/{{ ds }}",
        network_mode="bridge",
        task_id="docker-airflow-download",
        do_xcom_push=False,
        mount_tmp_dir=False,
        # !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )
    
    
    wait_data = FileSensor(
        task_id="wait_for_processed_data",
        filepath="processed/{{ ds }}/data.csv",
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke",
    )
    
    wait_target = FileSensor(
        task_id="wait_for_processed_target",
        filepath="processed/{{ ds }}/target.csv",
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke",
    )
    
    
    split = DockerOperator(
        image="airflow-split",
        command="--input-dir /data/processed/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )

    
    train = DockerOperator(
        image="airflow-train",
        command="--input-dir /data/processed/{{ ds }} --output-dir /data/model/{{ ds }}",
        task_id="docker-airflow-train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )
    
    
    validate = DockerOperator(
        image="airflow-validate",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/model/{{ ds }} --output-dir /data/metrics/{{ ds }}",
        task_id="docker-airflow-validate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )

    download >> preprocess >> [wait_data, wait_target] >> split >> train >> validate
