import pickle
from typing import Dict, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.pipeline import Pipeline

from entities.training_params import TrainingParams

SklearnClfModel = Union[RandomForestClassifier, LogisticRegression]


def train_model(
    features: pd.DataFrame, target: pd.Series, training_params: TrainingParams
) -> SklearnClfModel:
    if training_params.model_type == 'RandomForestClassifier':
        model = RandomForestClassifier(
            n_estimators=training_params.model_params['n_estimators']
        )
    elif training_params.model_type == 'LogisticRegression':
        model = LogisticRegression(max_iter=training_params.model_params['max_iter'])
    else:
        raise NotImplementedError()
    model.fit(features, target)
    return model


def predict_model(
    model: Pipeline, features: pd.DataFrame
) -> np.ndarray:
    predicts = model.predict(features)
    return predicts


def evaluate_model(
    predicts: np.ndarray, target: pd.Series
) -> Dict[str, float]:

    return {
        'precision': precision_score(target, predicts),
        'recall': recall_score(target, predicts),
        'accuracy': accuracy_score(target, predicts)
    }


def create_inference_pipeline(
    model: SklearnClfModel, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([('feature_part', transformer), ('model_part', model)])


def serialize_model(model: object, output: str) -> str:
    with open(output, 'wb') as f:
        pickle.dump(model, f)
    return output

