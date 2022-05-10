import pandas as pd
import numpy as np

#import sys
#sys.path.append('../')

from data.make_dataset import read_data, split_train_val_data
from train_pipeline import train_pipeline
from predict_pipeline import predict_pipeline

    
def test_read_data(input_data_path):
    data = read_data(input_data_path)
    assert isinstance(data, pd.DataFrame)
    assert data.shape == (297, 14)
    assert data.iloc[3, 4] == 282
    
def test_split_train_val_data(fake_X, fake_y, splitting_params):
    X_train, X_val, y_train, y_val = split_train_val_data(fake_X, fake_y, splitting_params)
    assert X_train.shape == (80, 13)
    assert X_val.shape == (20, 13)
    assert X_val.shape[0] == y_val.shape[0]
    
    
def test_train_pipeline(config_path):
    _, metrics = train_pipeline(config_path)
    assert metrics['accuracy'] > 0.5
    assert metrics['precision'] > 0.5
    assert metrics['recall'] > 0.5
    
def test_predict_pipeline(predict_config_path):
    predictions, _ = predict_pipeline(predict_config_path)
    assert len(predictions) > 0
    assert np.array_equal(np.unique(np.array(predictions)), np.array([0, 1]))

