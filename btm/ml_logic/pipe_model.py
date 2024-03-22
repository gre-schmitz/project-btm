import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.impute import KNNImputer
from xgboost import XGBRegressor
from btm.ml_logic.data import load_data
import pickle
import csv


def pipe(data_source: str):
    '''
    - Input will be our csv that has been turned into a DataFrame
    - Output will be a preprocessed X and y
    '''
    targets = ['Final_GDP_Interp', 'SPX Index ']
    models_params = ['best_params_GDP.csv','best_params_SPX.csv']

    loaded_data = {}
    for target in targets:
        X, y = load_data(data_source, target)
        loaded_data[target] = {
            f"X_{target}": X,
            f"y_{target}": y
        }


    # Initialize an empty dictionary to store the loaded data
    all_loaded_params = {}

    # Read the CSV file and populate the dictionary
    for params,target in zip(models_params,targets):
        loaded_params = {}
        with open(params, mode='r') as file:
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
        model = XGBRegressor(**all_loaded_params[target])
        pipes[target] = make_pipeline(preproc_selector, model)
        print(all_loaded_params[target])

        pipes[target].fit(loaded_data[target][f'X_{target}'], loaded_data[target][f'y_{target}'])

        with open(f"{target}.pkl", "wb") as file:
            pickle.dump(pipes[target], file)
    return pipes

#change
if __name__ == '__main__':
    pipe('/Users/javierasua/code/tbow27/project-btm/gdpnow_hf.csv')
