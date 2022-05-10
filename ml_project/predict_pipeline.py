import json
import logging
import os
import sys
from pathlib import Path

#import click
import pandas as pd
import pickle


from entities.predict_pipeline_params import (
    PredictingPipelineParams,
    read_predicting_pipeline_params,
)

from models.model_fit_predict import predict_model

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False
logger.info('Let the prediction begin! \n')

def predict_pipeline(config_path: str) -> str:
    predicting_pipeline_params = read_predicting_pipeline_params(config_path)

    test_data = pd.read_csv(predicting_pipeline_params.input_data_path, index_col=False)
    logger.info(f'data.shape is {test_data.shape} \n')
    
    with open(predicting_pipeline_params.input_model_path, 'rb') as f:
        model = pickle.load(f)

    y_pred = predict_model(model, test_data)
    y_pred_df = pd.DataFrame(y_pred)
    y_pred_df.to_csv(predicting_pipeline_params.output_predictions_path)

    logger.info(f'predictions are put at {predicting_pipeline_params.output_predictions_path}')

    return y_pred, predicting_pipeline_params.output_predictions_path

#@click.command(name='train_pipeline')
#@click.argument('config_path')
#def train_pipeline_command(config_path: str):
#    train_pipeline(config_path)
config_path = 'configs/predict_config.yaml'
predict_pipeline(config_path)

#if __name__ == '__main__':
#    train_pipeline_command()