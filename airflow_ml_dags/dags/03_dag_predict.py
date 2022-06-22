import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from docker.types import Mount
from airflow.models import Variable


default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "email_on_failure": True,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

model_path = Variable.get("model_path")

with DAG(
        "03_dag_predict",
        default_args=default_args,
        schedule_interval="@daily",
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

    
    wait_data = FileSensor(
        task_id="wait_for_raw_data",
        filepath="raw/{{ ds }}/data.csv",
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke",
    )
    
      
    predict = DockerOperator(
        image="airflow-predict",
        command="--input-dir /data/raw/{{ ds }} --model-path {{ var.value.model_path }} --output-dir /data/predictions/{{ ds }}",
        environment={"MODEL_PATH" : "{{ var.value.model_path }}"}, 
        task_id="docker-airflow-predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="C:/Users/zyvyhome/airflow-examples/data/", target="/data", type='bind')]
    )
    

    download >> wait_data >> predict 
