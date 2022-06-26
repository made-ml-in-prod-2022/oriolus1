import os
import pandas as pd
import numpy as np
import pickle
import requests
import logging
import time
from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel, conlist, validator


PATH_TO_MODEL = 'http://gorodmus.ru/temp/model.pkl'
FEATURE_LIST = [ 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach' , 'exang', 'oldpeak', 'slope', 'ca', 'thal']
TIME_TO_SLEEP = 20
TIME_TO_EXIT = 120

logger = logging.getLogger(__name__)

app = FastAPI()
start_time = time.time()


class HeartModel(BaseModel):
    features: List[str]
    data: List[conlist(Union[int, float, None], min_items=13, max_items=13)]

    
    @validator('features')
    def correct_number_of_features(cls, v):
        if len(v) != len(FEATURE_LIST):
            raise ValueError('Incorrect number of features!')
        return v

    @validator('features')    
    def correct_set_of_features(cls, v):
        if set(v) > set(FEATURE_LIST):
            diff = set(v) - set(FEATURE_LIST)
            raise ValueError(f'Features {diff} are missing')
        if set(v) < set(FEATURE_LIST):
            diff = set(FEATURE_LIST) - set(v)
            raise ValueError(f'Features {diff} are not supposed to be here')
        return v
    
    @validator('features')
    def correct_order_of_features(cls, v):
        if v != FEATURE_LIST:
            raise ValueError('Order of features is incorrect')
        return v
    
class HeartResponse(BaseModel):
    idx: int
    target: int


def make_prediction(features: List[str], data: List, model) -> List[HeartResponse]:
    idx = np.arange(0, len(data))
    data = pd.DataFrame(data, columns=features)
    pred = model.predict(data)
    pred = pd.DataFrame(pred)
    return [HeartResponse(idx=int(idx_), target=target) for idx_, target in zip(idx, pred[0])]


@app.get('/')
def read_root():
    return {'Hello world'}


@app.on_event('startup')
def load_model():
    global model
    
    time.sleep(TIME_TO_SLEEP)
    
    #model_path = os.getenv('PATH_TO_MODEL')
    model_path = PATH_TO_MODEL
    if model_path is None:
        err = f'PATH_TO_MODEL {model_path} is None'
        logger.error(err)
        raise RuntimeError(err)
    
    response = requests.get(model_path) 
    
    with open('model_file.pkl', 'wb') as f:
        f.write(response.content)
        f.close()
        
    with open('model_file.pkl', 'rb') as f:
        model = pickle.load(f)
        return model    



@app.get('/health/')
def health() -> bool:
    global start_time
    elapsed_time = time.time() - start_time
    if elapsed_time > TIME_TO_EXIT:
        raise Exception("App exited, farewell!")
    
#    if model == True:
#        return 200
#    else:
#        return 404
    return not(model is None)


@app.get('/predict/', response_model=List[HeartResponse])
def predict(request: HeartModel):
    return make_prediction(request.features, request.data, model)






#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8000)