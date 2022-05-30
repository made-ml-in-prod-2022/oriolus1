import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
import pytest

from app import app


@pytest.fixture()
def features_for_testing():
    data = pd.read_csv('fake_data.csv')
    request_features = list(data.columns)
    return request_features


@pytest.fixture()
def data_for_testing():
    data = pd.read_csv('fake_data.csv')
    request_data = data.values.tolist()
    return request_data


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_predict(features_for_testing, data_for_testing):
    with TestClient(app) as client:
        number_of_requests = len(data_for_testing)
        print(data_for_testing)
        response = client.get(
            'http://127.0.0.1:8000/predict/',
            json={'features': features_for_testing, 'data': data_for_testing}
        )
        response_json = response.json()
        predictions = [response_json[i]['target'] for i in range(0, number_of_requests)]
        assert response.status_code == 200
        assert len(predictions)==number_of_requests
        assert np.array_equal(np.unique(np.array(predictions)), np.array([0, 1]))
        assert predictions==[1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
        