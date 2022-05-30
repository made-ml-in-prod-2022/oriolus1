import pandas as pd
import requests

from pydantic import ValidationError
from app import HeartModel
  
        
if __name__ == '__main__':
    data = pd.read_csv('fake_data.csv')
    request_features = list(data.columns)
    print(f'Request features are {request_features}\n')
    request_data = data.values.tolist()
    print(f'Request data is {request_data}\n')
    
    try: 
        HeartModel(features=request_features, data=request_data)
    except ValidationError as e:
        print(e)
    
    response = requests.get(
        'http://127.0.0.1:8000/predict/',
        json={'features': request_features, 'data': request_data},
    )
    print(f'Status code is {response.status_code}\n')
    print(f'Prediction is {response.json()}\n')
        