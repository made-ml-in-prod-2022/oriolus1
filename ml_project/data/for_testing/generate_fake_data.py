import pandas as pd
from faker import Faker

TEST_SIZE = 100
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

fake_data.to_csv('fake_data.csv', index=False)