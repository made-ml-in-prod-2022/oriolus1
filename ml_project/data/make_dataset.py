import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from entities.splitting_params import SplittingParams


def read_data(input_data_path: str) -> pd.DataFrame:
    return pd.read_csv(input_data_path)


def split_train_val_data(X: pd.DataFrame, y: pd.Series, params: SplittingParams) -> Tuple[
        pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

    if params.stratify == 'yes':
        stratify = y
    else:
        stratify = None
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, 
        test_size=params.val_size, 
        random_state=params.random_state, 
        stratify=stratify
        )
    
    return X_train, X_val, y_train, y_val 