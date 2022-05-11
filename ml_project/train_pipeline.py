import json
import logging
import os
import sys
from pathlib import Path
from typing import Tuple, List

#import click
import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from ml_project.custom_transformer import CustomTransformer

from ml_project.data.make_dataset import read_data, split_train_val_data
from ml_project.entities.train_pipeline_params import (
    TrainingPipelineParams,
    read_training_pipeline_params,
)
#from features import make_features
#from features.build_features import extract_target, build_transformer
from ml_project.models.model_fit_predict import (
    train_model,
    create_inference_pipeline,
    predict_model,
    evaluate_model,
    serialize_model
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False
logger.info('Let the adventure begin! \n')

def train_pipeline(config_path: str) -> Tuple[str, List[float]]:
    training_pipeline_params = read_training_pipeline_params(config_path)

    data = read_data(training_pipeline_params.input_data_path)
    logger.info(f'data.shape is {data.shape} \n')
    
    target_col = training_pipeline_params.feature_params.target_col
    y = data[target_col]
    X = data.drop(columns=[target_col])
    
    logger.info('splitting data to train and val')
    if training_pipeline_params.splitting_params.stratify == 'yes':
        logger.info('stratification (by target) is used \n')

    X_train, X_val, y_train, y_val = split_train_val_data(
        X, y, training_pipeline_params.splitting_params
        )

    logger.info(f'X_train.shape is {X_train.shape}')
    logger.info(f'X_val.shape is {X_val.shape} \n')
    
    transformer = ColumnTransformer(
        transformers=[
                ('custom', CustomTransformer(), training_pipeline_params.feature_params.special_feature), 
                ('scaler', StandardScaler(), training_pipeline_params.feature_params.numerical_features), 
                ('ohe', OneHotEncoder(), training_pipeline_params.feature_params.categorical_features)
            ], remainder='drop'
    )


    transformer.fit(X_train)
    X_train = transformer.transform(X_train)
    logger.info('transformer is applied:')
    logger.info(f'    one-hot encoding to {training_pipeline_params.feature_params.categorical_features}')
    logger.info(f'    standard scaler to {training_pipeline_params.feature_params.numerical_features}')    
    if training_pipeline_params.feature_params.features_to_drop is not None:
        logger.info(f'dropping features: {training_pipeline_params.feature_params.features_to_drop}')
    #transformer = build_transformer(training_pipeline_params.feature_params)
    #transformer.fit(train_df)

    logger.info(f'\n model type is: {training_pipeline_params.training_params.model_type}')
    logger.info(f'model params are: {training_pipeline_params.training_params.model_params}\n')

    model = train_model(X_train, y_train, training_pipeline_params.training_params)

    inference_pipeline = create_inference_pipeline(model, transformer)
    
    y_val_pred = predict_model(inference_pipeline, X_val)
   
    metrics = evaluate_model(y_val_pred, y_val)
    logger.info(f'validation metrics are {metrics}')

    path_to_model = serialize_model(
        inference_pipeline, training_pipeline_params.output_model_path
    )
    
    return path_to_model, metrics


#    with open(training_pipeline_params.metric_path, 'w') as metric_file:
#        json.dump(metrics, metric_file)
#    logger.info(f'metrics is {metrics}')




#@click.command(name='train_pipeline')
#@click.argument('config_path')
#def train_pipeline_command(config_path: str):
#    train_pipeline(config_path)
config_path = 'ml_project/configs/forest_train_config.yaml'
train_pipeline(config_path)

#if __name__ == '__main__':
#    train_pipeline_command()