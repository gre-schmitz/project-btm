from btm.ml_logic.preprocessor import preprocessing_data
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

def fitting():

    # Instantiating model
    model_best =  XGBRegressor(
        n_estimators=200,
        max_depth = 9,
        learning_rate = 0.275,
        random_state=42,
        reg_lambda = 0.01)

    X, y = preprocessing_data
    model_best.fit(X, y)
    return model_best
