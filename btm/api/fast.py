import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from btm.ml_logic.pipe_model import pipe
from btm.ml_logic.data import load_data
from datetime import datetime

app = FastAPI()
app.state.model = pipe('train_set.csv')

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
    return dict(greeting="Hello, welcome to our BTM-API!")

@app.get("/latest_gdp_predictions")
def predict_gdp():
    #turning our prediction.csv into a DataFrame
    model = app.state.model
    X_dropped, y_dropped = load_data('test_set.csv')
    y_pred = model.predict(X_dropped)
    dict_out = {}
    for i, y in enumerate(y_pred):
        dict_out[X_dropped.index[i].to_pydatetime().strftime('%Y-%m-%d')] = \
            float(y)

    return dict_out
