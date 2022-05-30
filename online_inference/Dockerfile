FROM python:3.9

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py

COPY fake_data.csv fake_data.csv

COPY make_predict.py make_predict.py

COPY test_predict.py test_predict.py

ENV PATH_TO_MODEL="http://gorodmus.ru/temp/model.pkl"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
