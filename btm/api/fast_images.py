import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from btm.ml_logic.pipe_model import pipe
from btm.ml_logic.data_predictions import load_data_predictions
from datetime import datetime
import pickle
import os
from io import BytesIO
import shap
from shap import Explanation
from shap.plots import waterfall
import matplotlib.pyplot as plt
plt.switch_backend('Agg') #telling plt that we are working in a backend (with no graphic rendering)

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
    base_url = "https://btm-final-4yiq46myaq-ew.a.run.app"
    return {
            "greeting": "Hello, welcome to our BTM-API!",
            "links": {
                "latest_gdp_predictions": f"{base_url}/latest_gdp_predictions",
                "latest_spx_predictions": f"{base_url}/latest_spx_predictions",
                "download_picture": f"{base_url}/download_picture"

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
    X_dropped, y_dropped = load_data_predictions('total_df_w_btm.csv','SPX Index ')
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
    # print(df_plot_life)
    # Print the updated DataFrame
    # print(df_plot_life)


    all_predictions = {
        'title' :'SPX Index Predictions',
        'df' : df_plot_life.to_dict()
    }


    return all_predictions

# @app.get("/prediction_set")
# def predict_set():
#     Target = 'SPX Index '
#     Drop = ['Quarter being forecasted', 'Advance Estimate From BEA',
#             'Publication Date of Advance Estimate','Days until advance estimate',
#             'Forecast Error', 'Data releases', 'NDX Index ', 'SPX Index ']

#     test = pd.read_csv('predict_set_w_btm.csv', index_col='Dates', parse_dates=True) #date_parser=dateparse)
#     X_test = test.drop(columns=Drop)
#     # y_test = test[Target]

#     prediction_set = {'title': 'prediction set for current quarter',
#                       'df': X_test.to_dict()}

#     return prediction_set




@app.get("/download_picture")
def download_picture():
    model = app.state.spx
    #X_dropped, y_dropped = load_data_predictions('predict_set_w_btm.csv','SPX Index ')
    X_dropped, y_dropped = load_data_predictions('total_df_w_btm.csv','SPX Index ')

    # Define the mapping of original feature names to new, interpretable names
    feature_name_map = {
        'value_CCLACBW027SBOG': 'CreditCards_Loans',
        'value_WTISPLC': 'WTI_Price',
        'value_EXPINF1YR': 'Infl_Exp_1Y_Surv',
        'value_STLPPM': 'Gold_Price',
        'value_M2REAL': 'Real_M2',
        'value_UNRATE': 'Unemp_Rate',
        'value_PPIACO': 'All_ProducerPrices',
        'value_PCUOMFGOMFG': 'Mfg_ProducerPrices',
        'value_PCUATRANSATRANS': 'Transport_ProducerPrices',
        'value_PCUATRADEATRADE': 'Trade_ProducerPrices',
        'value_PCUAWHLTRAWHLTR': 'Wholesale_ProducerPrices',
        'value_CSUSHPINSA': 'Home_Prices',
        'value_SPCS20RSA': 'S&P_20_City_Home_Prices',
        'value_WALCL': 'FedReserve_Assets',
        'value_REAINTRATREARAT10Y': 'Real_Rates_10Y',
        'value_SAHMREALTIME': 'Sahm_Rule',
        'value_POPTHM': 'Population',
        'value_CES0500000003': 'Avg_Hourly_Earn',
        'value_NFCI': 'ChiFed_NFCI',
        'value_WEI': 'Weekly_Econ_Ind',
        'value_ICSA': 'Initial_Jobless_Claims',
        'value_ADPWNUSNERSA': 'ADP_Employment',
        'value_FEDFUNDS': 'Fed_Funds_Rate',
        'value_CORESTICKM159SFRBATL': 'Core_Infl',
        'value_CPIAUCSL': 'CPI',
        'value_PAYEMS': 'Nonfarm_Employ',
        'value_MORTGAGE30US': 'Mortgage_30Y',
        'USGGBE02 Index': 'US_2Y_Infl_Market_Hedge_Price',
        'USOSFR10 Curncy': 'USD_10Y_IR',
        'CL1 Comdty': 'Oil_Futures',
        'GSUSFCI Index': 'GS_FinCond_Index',
        'CESIUSD Index': 'Citi_EconSupr_Index',
        'Monthly Nominal GDP Index': 'Nom_GDP_Mo',
        'Monthly Real GDP Index': 'Real_GDP_Mo',
        'Structures': 'Construction',
        'USOSFR2 Curncy': 'USD_2Y_Interest_Rate',
        }

    # Prepare the last observation for SHAP analysis
    #breakpoint()
    last_index = X_dropped.index[-15]
    X_waterfall = X_dropped.loc[last_index:]
    print(X_waterfall.shape)
    #breakpoint()
    # Compute SHAP values for the last observation
    explainer = shap.Explainer(model.predict, X_waterfall)
    shap_values = explainer(X_waterfall)

    # Apply the mapping to the SHAP values feature names
    # This step assumes shap_values.data is a DataFrame; if not, adjust as necessary
    if hasattr(shap_values, 'feature_names'):
        shap_values.feature_names = [feature_name_map.get(name, name) for name in shap_values.feature_names]

    # # # # For visualization like waterfall, which typically uses the base_values and feature values
    # # # # The feature names can be directly mapped in the visualization step if not inherent to the SHAP values object
    # shap.summary_plot(shap_values, max_display=10, feature_names=[feature_name_map.get(name, name) for name in X_dropped.columns])

    # Assuming 'shap_values' is already computed for 'X_waterfall'
    # Let's assume 'shap_values_one' represents the SHAP values for the last observation
    shap_values_one = shap_values[-1]

    # Map feature names from 'X_dropped.columns' to the names in 'feature_name_map'
    mapped_feature_names = [feature_name_map.get(name, name) for name in X_dropped.columns]

    # Create an Explanation object with mapped feature names
    exp = Explanation(values=shap_values_one.values,
                    base_values=shap_values_one.base_values,
                    data=shap_values_one.data,
                    feature_names=mapped_feature_names)

    # Use the waterfall plot for the Explanation object
    waterfall(exp, show=False).savefig('scratch.png',format = "png",dpi = 150,bbox_inches = 'tight')


    return FileResponse('scratch.png')
