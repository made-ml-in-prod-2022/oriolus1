

Запуск докера через файл:

docker build -t oriolus1/hw2:v1 .

docker run -p 8000:8000 oriolus1/hw2:v1

Запуск докера через докер-хаб:

docker pull oriolus1/hw2:v1 .

docker run -p 8000:8000 oriolus1/hw2:v1

Скрипт, который делает запросы к сервису:

python make_predict.py

Тестирование предикта:

pytest test_predict.py
