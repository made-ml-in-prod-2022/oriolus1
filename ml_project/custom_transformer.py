
from dataclasses import dataclass, field
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


@dataclass()
class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        return None
    
    def fit(self, X):
        return self
    
    def transform(self, X, feature_name='oldpeak'):
        X_ = X.copy()
        X_[feature_name] = 1 / (X_[feature_name] + np.mean(X_[feature_name]))
        return X_