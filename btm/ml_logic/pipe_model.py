import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.impute import KNNImputer
from xgboost import XGBRegressor
from btm.ml_logic.data import load_data
import pickle


def pipe(data_source: str):
    '''
    - Input will be our csv that has been turned into a DataFrame
    - Output will be a preprocessed X and y
    '''
    X_dropped, y_dropped = load_data(data_source)

    # sklearn pipeline
    # first part of the pipeline will impute the few NAs and scale the data
    preproc = Pipeline([
        ('imputer', KNNImputer(n_neighbors=5)),
        ('scaler', RobustScaler())
    ])

    preproc_selector = Pipeline([
        ('preprocessing', preproc),  # Include the preprocessing steps
        # GridSearch has shown that keeping 43% of or features maximizes
        # the model's performance out test set
        ('feature_selection', SelectPercentile(
            mutual_info_regression,
            percentile=43 #
        ))
    ])

    model_best =  XGBRegressor(
        n_estimators=200,
        max_depth = 9,
        learning_rate = 0.275,
        random_state=42,
        reg_lambda = 0.01)

    pipe_best = make_pipeline(preproc_selector, model_best)

    pipe_best.fit(X_dropped, y_dropped)

    with open("pipeline.pkl", "wb") as file:
        pickle.dump(pipe_best, file)

    return pipe_best

#change
if __name__ == '__main__':
    pipe('/Users/javierasua/code/tbow27/project-btm/gdpnow_hf.csv')
