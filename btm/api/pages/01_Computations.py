import streamlit as st
import requests
import pandas as pd
from PIL import Image
import pickle
import shap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


url_spx = 'https://btm-final-4yiq46myaq-ew.a.run.app/latest_spx_predictions'
url_predict = 'https://btm-final-4yiq46myaq-ew.a.run.app/prediction_set'

response_spx = requests.get(url_spx).json()
response_predict = requests.get(url_predict).json()


st.markdown("# __Beat the Market__ #")
"__Come to the Data Science side of trading and try to **b**eat **t**he **m**arket with us!__"

"We are using Machine Learning to compute fair values of the S&P 500!"

st.markdown('<hr>', unsafe_allow_html=True)

"## Calculate fair values ##"



"Ready to get your hands dirty? Let's see today's signals!"
""
"(This might take a minute, things are actually being calculated...)"

#############################################################################
### waterfall ###############################################################
#############################################################################
# Target = 'SPX Index '
# Drop = ['Quarter being forecasted', 'Advance Estimate From BEA',
#         'Publication Date of Advance Estimate','Days until advance estimate',
#         'Forecast Error', 'Data releases', 'NDX Index ', 'SPX Index ']

# test = pd.read_csv('predict_set_w_btm.csv', index_col='Dates', parse_dates=True) #date_parser=dateparse)
# X_test = test.drop(columns=Drop)
# y_test = test[Target]

# X_test = pd.DataFrame(response_predict['df'])
# X_test.index = pd.to_datetime(X_test.index)
# # st.write(X_test.head())

# model = pickle.load(open('spx_final_pickle.pkl',"rb"))

# explainer = shap.Explainer(model.predict, X_test)
# st.session_state.explainer = None
# shap_values = explainer(X_test)
# st.session_state.shap_values = None



st.set_option('deprecation.showPyplotGlobalUse', False)

#get!!!
# df = get_dataframe_data()
if st.button('get latest computations'):
    # print is visible in the server output, not in the page
    print('button clicked!')

    col1, col2, col3 = st.columns(3)
    col1.metric("GDP real time",
            round(list(response_spx['df']['BTM GDP'].values())[-1],2),
            round(list(response_spx['df']['BTM GDP'].values())[-1] - \
                list(response_spx['df']['BTM GDP'].values())[-2],2))
    # col2.metric('S&P 500 index',
    #         list(response_spx['df']['Market'].values())[-1],
    #         round(list(response_spx['df']['Market'].values())[-1] - \
    #             list(response_spx['df']['Market'].values())[-2],2))
    col2.metric('S&P 500 index',
            5248.49,
            round(5248.49 - \
                5251,25))
    col3.metric("S&P Fair Value",
            round(list(response_spx['df']['BTM Model'].values())[-1], 2),
            round(list(response_spx['df']['BTM Model'].values())[-1] - \
                list(response_spx['df']['BTM Model'].values())[-2],2))

    # Now come the implications
    ""
    f"Based on our calculations from 2024-03-27 we provide the following signal"

    if list(response_spx['df']["Action"].values())[-1] == 'Fair Value':
        "#### Hold tight and do nothing 🤷‍♂️ ####"
        '> "Make a few great investments and just sit on your ass"\t\n\nCharlie Munger'
    elif list(response_spx['df']["Action"].values())[-1] == 'Strong Sell':
        "#### S&P seems *over*valued. Sell! Sell! Sell! 📉 ####"
        '> "Time to say good bye"\t\n\nAndrea Bocelli'
    elif list(response_spx['df']["Action"].values())[-1] == 'Sell':
        "#### S&P seems slightly *over*valued. Consider reducing your S&P exposure moderately... 🤔 ####"
        '> "Don\'t cry because it\'s over, smile because it happened."\t\n\nDr Seuss'
    elif list(response_spx['df']["Action"].values())[-1] == 'Buy':
        "#### S&P seems slightly *under*valued. Consider going moderately long your S&P exposure... 🤔 ####"
        '> "You can\'t start a fire without a little spark"\t\n\nBruce Springsteen'
    elif list(response_spx['df']["Action"].values())[-1] == 'Strong Buy':
        "#### S&P seems *under*valued. Buy! Buy! Buy!... 📈 ####"
        '> "\'Cos opportunity comes once in a lifetime"\t\n\nEminem'


    "## What is driving our predictions? ##"

    """It can be spooky to be told stories by Machine Learning algorithms. Let us
    explain what is driving our predictions."""
    ""
#if st.button('find out about our drivers'):
    # print is visible in the server output, not in the page
    #print('button clicked!')
    "##### Our prediction's main drivers: #####"
    st.markdown('<hr>', unsafe_allow_html=True)

    url = 'https://btm-final-4yiq46myaq-ew.a.run.app/download_picture'
    response = requests.get(url)

    st.image(response.content)

    """**Explanation:** The listed features from above tell you wether they have driven
    the S&P's fair value up (red arrows) or down (blue arrows) compared to last years'
    average value of the actual S&P."""



st.markdown('<hr>', unsafe_allow_html=True)

st.write("### How do we do it?")
st.markdown("Let us introduce [our concept](Background).")
