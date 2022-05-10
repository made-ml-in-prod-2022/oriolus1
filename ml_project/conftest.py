import pandas as pd
from faker import Faker
from entities.splitting_params import SplittingParams
import pytest

TEST_SIZE = 100

@pytest.fixture()
def input_data_path() -> str:
    return 'data/raw/heart_cleveland_upload.csv'


@pytest.fixture()
def fake_X() -> pd.DataFrame:
    faker = Faker()
    fake_data = pd.DataFrame({
        'age': [faker.pyint(min_value=29, max_value=77) for _ in range(TEST_SIZE)],
        'sex': [faker.pyint(min_value=0, max_value=1) for _ in range(TEST_SIZE)],
        'cp': [faker.pyint(min_value=0, max_value=3) for _ in range(TEST_SIZE)],
        'trestbps': [faker.pyint(min_value=94, max_value=200) for _ in range(TEST_SIZE)],
        'chol': [faker.pyint(min_value=126, max_value=564) for _ in range(TEST_SIZE)],
        'fbs': [faker.pyint(min_value=0, max_value=1) for _ in range(TEST_SIZE)],
        'restecg': [faker.pyint(min_value=0, max_value=2) for _ in range(TEST_SIZE)],
        'thalach': [faker.pyint(min_value=71, max_value=202) for _ in range(TEST_SIZE)],
        'exang': [faker.pyint(min_value=0, max_value=1) for _ in range(TEST_SIZE)],
        'oldpeak': [faker.pyfloat(min_value=0, max_value=6.2) for _ in range(TEST_SIZE)],
        'slope': [faker.pyint(min_value=0, max_value=2) for _ in range(TEST_SIZE)],
        'ca': [faker.pyint(min_value=0, max_value=3) for _ in range(TEST_SIZE)],
        'thal': [faker.pyint(min_value=0, max_value=2) for _ in range(TEST_SIZE)],
    })
    
    return fake_data


@pytest.fixture()
def fake_y() -> pd.DataFrame:
    faker = Faker()
    fake_data = pd.DataFrame({
        'condition': [faker.pyint(min_value=0, max_value=1) for _ in range(TEST_SIZE)]
    })
    
    return fake_data


@pytest.fixture()
def splitting_params() -> SplittingParams:
    return SplittingParams(val_size=0.2, random_state=0, stratify='yes')


@pytest.fixture()
def config_path() -> str:
    return 'configs/forest_train_config.yaml'


@pytest.fixture()
def predict_config_path() -> str:
    return 'configs/predict_config.yaml'
