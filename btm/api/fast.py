import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from btm.ml_logic.pipe_model import pipe
from btm.ml_logic.data_predictions import load_data_predictions
from datetime import datetime
import pickle
import os
from io import BytesIO

#change
app = FastAPI()
targets = ['Final_GDP_Interp', 'SPX Index ']


app.state.gdp = pickle.load(open('Final_GDP_Interp.pkl',"rb"))
app.state.spx = pickle.load(open('spx_final_pickle.pkl',"rb"))


# Allowing all middleware is optional,
# but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    base_url = "http://127.0.0.1:8000"
    return {
            "greeting": "Hello, welcome to our BTM-API!",
            "links": {
                "latest_gdp_predictions": f"{base_url}/latest_gdp_predictions",
                "latest_spx_predictions": f"{base_url}/latest_spx_predictions"

                }
    }

@app.get("/latest_gdp_predictions")
def predict_gdp():
    #turning our prediction.csv into a DataFrame
    model = app.state.gdp
    X_dropped, y_dropped = load_data_predictions('predict_set.csv','Final_GDP_Interp')
    y_pred = model.predict(X_dropped)
    dict_out = {}
    for i, y in enumerate(y_pred):
        dict_out[X_dropped.index[i].to_pydatetime().strftime('%Y-%m-%d')] = \
            float(y)

    all_predictions = {
        'title' :'GDP Predictions',
        'predictions' : dict_out
    }
    return all_predictions

@app.get("/latest_spx_predictions")
def predict_spx():
    #turning our prediction.csv into a DataFrame
    model = app.state.spx
    X_dropped, y_dropped = load_data_predictions('predict_set_w_btm.csv','SPX Index ')
    y_pred = model.predict(X_dropped)
    dict_out = {}
    for i, y in enumerate(y_pred):
        dict_out[X_dropped.index[i].to_pydatetime().strftime('%Y-%m-%d')] = \
            float(y)



    predictions_life = model.predict(X_dropped)

    predictions_life = pd.Series(predictions_life)
    predictions_life.index = y_dropped.index

    df_plot_life = pd.DataFrame()
    btm_gdp  = X_dropped['Final_GDP_Interp']

    df_plot_life = pd.concat([y_dropped, predictions_life, btm_gdp], axis=1)
    df_plot_life.info()

    df_plot_life['Market'] = df_plot_life['SPX Index ']
    df_plot_life['BTM Model'] = df_plot_life[0]
    df_plot_life['Diff'] = df_plot_life['SPX Index '] - df_plot_life[0]
    df_plot_life = df_plot_life.drop(columns=['SPX Index ', 0])
    df_plot_life['Diff Z-score'] = (df_plot_life['Diff'] - df_plot_life['Diff'].mean()) / df_plot_life['Diff'].std()

    conditions = [
    (df_plot_life['Diff Z-score'] > 2.5),
    (df_plot_life['Diff Z-score'] > 1.5),
    (df_plot_life['Diff Z-score'] < -2.5),
    (df_plot_life['Diff Z-score'] < -1.5)
    ]

    df_plot_life['BTM GDP'] = df_plot_life['Final_GDP_Interp'].fillna(method='ffill')
    df_plot_life = df_plot_life.drop(df_plot_life.columns[0], axis=1)

    values = ['Strong Sell', 'Sell', 'Strong Buy','Buy']

    # Create a new column 'Action' based on conditions and values
    df_plot_life['Action'] = np.select(conditions, values, default='Fair Value')
    print(df_plot_life)
    # Print the updated DataFrame
    print(df_plot_life)


    all_predictions = {
        'title' :'SPX Index Predictions',
        'df' : df_plot_life.to_dict()
    }





    """ model = app.state.spx
    X_dropped, y_dropped = load_data_predictions('predict_set_w_btm.csv', 'SPX Index ')
    y_pred = model.predict(X_dropped)

    # Get the last datetime and prediction
    last_index = X_dropped.index[-1].to_pydatetime().strftime('%Y-%m-%d')
    last_prediction = float(y_pred[-1])

    # Create the dictionary with only the last datetime and prediction
    dict_out = {last_index: last_prediction}

    all_predictions = {
        'title': 'SPX Index Predictions',
        'predictions': dict_out
    } """




    return all_predictions
