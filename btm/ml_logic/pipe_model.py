import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.impute import KNNImputer
from xgboost import XGBRegressor
from btm.ml_logic.data import load_data
from btm.ml_logic.data_predictions import load_data_predictions
import pickle
import csv
import os

def pipe(data_source: str):
    '''
    - Input will be our csv that has been turned into a DataFrame
    - Output will be a preprocessed X and y
    '''
    targets = ['Final_GDP_Interp', 'SPX Index ']
    models_params = ['best_params_GDP.csv','best_params_SPX.csv']

    abs_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(abs_path,data_source)


    loaded_data = {}
    for target in targets:

        with_btm_data_X, with_btm_data_y = load_data_predictions(os.path.join(abs_path,'predict_set_w_btm.csv'),target)

        X, y = load_data(file_path, target)
        if target == 'SPX Index ':
            X = pd.concat([X, with_btm_data_X])
            y = pd.concat([y, with_btm_data_y])
            print(X)

        loaded_data[target] = {
            f"X_{target}": X,
            f"y_{target}": y
        }

        print(loaded_data[target])

    # Initialize an empty dictionary to store the loaded data
    all_loaded_params = {}

    # Read the CSV file and populate the dictionary
    for params,target in zip(models_params,targets):
        params_path = os.path.join(abs_path,params)
        loaded_params = {}
        with open(params_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                param_name = row['Parameter']
                if row['Value'].isdecimal():
                    param_value = int(row['Value'])
                else :
                    param_value = float(row['Value'])
                loaded_params[param_name] = param_value
        all_loaded_params[target] = loaded_params
    print(all_loaded_params)
    # sklearn pipeline
    # first part of the pipeline will impute the few NAs and scale the data

    pipes = {}
    for target in targets:
        preproc = Pipeline([
            ('imputer', KNNImputer(n_neighbors=all_loaded_params[target]['n_neighbors'])),
            ('scaler', RobustScaler())
        ])

        preproc_selector = Pipeline([
            ('preprocessing', preproc),  # Include the preprocessing steps
            # GridSearch has shown that keeping 43% of or features maximizes
            # the model's performance out test set
            ('feature_selection', SelectPercentile(
                mutual_info_regression,
                percentile=all_loaded_params[target]['percentile'] #
            ))
        ])
        model = XGBRegressor(**all_loaded_params[target])
        pipes[target] = make_pipeline(preproc_selector, model)

        pipes[target].fit(loaded_data[target][f'X_{target}'], loaded_data[target][f'y_{target}'])

        with open(f"{target.replace(' ','')}.pkl", "wb") as file:
            pickle.dump(pipes[target], file)
    return pipes

#change
if __name__ == '__main__':
    pipe('train_set.csv')
