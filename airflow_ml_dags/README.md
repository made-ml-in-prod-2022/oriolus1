Запустить airflow:

cd images\airflow-ml-base\

docker build . -t airflow-ml-base:latest

docker-compose up --build

Потом надо прописать вручную в Airflow UI в connections в поле Extra: {"path": "/opt/airflow/data"}

И в Variable сейчас предполагается поставить переменную model_path со значением /data/model/2022-06-22/model.pkl 
Но можно делать что-то еще.