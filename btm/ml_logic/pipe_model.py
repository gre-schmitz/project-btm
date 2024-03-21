import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.impute import KNNImputer
from xgboost import XGBRegressor
from btm.ml_logic.data import load_data


def pipe():
    '''
    - Input will be our csv that has been turned into a DataFrame
    - Output will be a preprocessed X and y
    '''
    data = load_data()

    # What is the target?
    Target = 'Final_GDP_Interp'

    # What features will be dropped in the first place?
    Drop = ['GDP Nowcast', 'Final_GDP_Interp', 'Quarter being forecasted',
            'Advance Estimate From BEA', 'Publication Date of Advance Estimate',
            'Days until advance estimate', 'Forecast Error', 'Data releases']

    # DataFrame will have a lot of empty rows. Lets drop these.
    # However, 2 rows of them sometimes are empty even when the rest is filled
    # Rows where only these two are missing will not be dropped

    data_dropped = data.dropna(axis=0, thresh=len(data.columns)-2)


    # Defining our X and y
    X_dropped = data_dropped.drop(columns=Drop)
    y_dropped = data_dropped[Target]

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

    return pipe_best
