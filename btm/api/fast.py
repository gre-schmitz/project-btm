import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from btm.ml_logic.pipe_model import pipe
from btm.ml_logic.data import load_data
from datetime import datetime
import pickle
import os

#change
app = FastAPI()
targets = ['Final_GDP_Interp', 'SPX Index ']


app.state.gdp = pickle.load(open('Final_GDP_Interp.pkl',"rb"))
app.state.spx = pickle.load(open('SPX Index .pkl',"rb"))


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
    X_dropped, y_dropped = load_data('predict_set.csv','Final_GDP_Interp')
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
    X_dropped, y_dropped = load_data('predict_set.csv','SPX Index ')
    y_pred = model.predict(X_dropped)
    dict_out = {}
    for i, y in enumerate(y_pred):
        dict_out[X_dropped.index[i].to_pydatetime().strftime('%Y-%m-%d')] = \
            float(y)

    all_predictions = {
        'title' :'SPX Index Predictions',
        'predictions' : dict_out
    }




    return all_predictions
