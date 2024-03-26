import streamlit as st
import requests
import pandas as pd
from PIL import Image

"# BTM #"
"__Come to the Data Science side of trading and try to **b**eat **t**he **m**arket with us!__"

"## Computing the GDP in real time ##"

"""The gross domestic product (=GDP) is the most important index in Economics.
No index covers the economic development as broadly as the GDP. While stock
markets are impacted by a broad spectrum of indices, the GDP is with no doubt
among the most important figures to determine prices.
"""

"""However, the GDP is announced only quarterly while stock prices change every
second!"""

"Wouldn't it be nice to see the GDP in real time?"
""
"""It would. But no one can. *However:* We might be close!"""

"""We went searching for the best data sources, ran them through our Machine Learning
model and produced promising results!"""

image_gdp_actual_predicted = Image.open('images/GDP_actual_vs_predicted.png')
st.image(image_gdp_actual_predicted, caption='Interpolated Actual vs predicted', use_column_width=True)

"""We have lineally interpolated the GDP between two official announcements and then trained
our model to predict these using more than 60 features!"""

"""Please note, that our model only works around a quarter ahead from today.
If you want to predict within that range, however, we believe we have a powerful
predictor regarding the GDP in real time!"""

"## Predicting the S&P 500 using our real time GDP ##"

"""Having a predictor for the real time GDP.. why don't we use it on the stock
market? Our idea is to calculate **fair values** for today's S&P and other
financial figures to help us find investing strategies."""

flowchart = Image.open('images/flowchart.png')
st.image(flowchart, caption='Basic idea of our webapp', use_column_width=True)

"""Again we have used a Machine Learning Model to find the connection of each
feature in our data set to the S&P"""

"""Our backwardly directed training gave our model a pretty good idea:"""

sp_backwards = Image.open('images/sp_backward.png')
st.image(sp_backwards, caption='Training our S&P model', use_column_width=True)

"""Making predictions for the current quarter looks promising (remember we do not
have official GDPs yet, just our live prediction)"""

sp_forward = Image.open('images/sp_forward.png')
st.image(sp_forward, caption="Our S&P model's performance", use_column_width=True)

"""What can we conclude now from this? We believe that our model's *predicted*
values for the S&P 500 can serve as a *fair value* of the S&P! If our model
is calculating a *lower* value than the actual price of the S&P, this is a buy
signal and vice versa! And also, if they are sufficiently alike... it is time
to grab a cold drink and do nothing."""

url_spx = 'http://localhost:8000/latest_spx_predictions'
url_gdp = 'http://localhost:8000/latest_gdp_predictions'

response_spx = requests.get(url_spx).json()

# Calculating
# @st.cache_resource
# def get_dataframe_data():
#     gdp_value = list(response_gdp['predictions'].values())[-1]
#     spx_value = list(response_spx['df']['Mkt'].values())[-1]
#     sps_fairvalue = list(response_spx['df']['Mdl'].values())[-1]
#     sps_diff_z = list(response_spx['df']["Diff Z-score"].values())[-1]
#     index_value = list(response_gdp['predictions'].keys())[-1]


#     return pd.DataFrame(
#         [[gdp_value, spx_value, sps_fairvalue, sps_diff_z]],
#         index=[index_value],
#         columns=['GDP real time prediction',
#                  'S&P 500 index',
#                  'S&P Fair Value',
#                  'Diff Z-Score']
#     )

"## Calculate fair values ##"

"Ready to get your hands dirty? Let's see today's signals!"

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
    col2.metric('S&P 500 index',
            list(response_spx['df']['Market'].values())[-1],
            list(response_spx['df']['Market'].values())[-1] - \
                list(response_spx['df']['Market'].values())[-2])
    col3.metric("S&P Fair Value",
            round(list(response_spx['df']['BTM Model'].values())[-1], 2),
            round(list(response_spx['df']['BTM Model'].values())[-1] - \
                list(response_spx['df']['BTM Model'].values())[-2],2))

    # Now come the implications
    ""
    f"Based on our calculations from {list(response_spx['df']['BTM GDP'].keys())[-1][:11]} we provide the following signal"

    if list(response_spx['df']["Action"].values())[-1] == 'Fair Value':
        "#### Hold tight and do nothing 🤷‍♂️ ####"
        '> "Make a few great investments and just sit on your ass"\t\n\nCharlie Munger'
    elif list(response_spx['df']["Action"].values())[-1] == 'Strong Sell':
        "#### S&P seems *over*valued. Consider reducing your S&P exposure... 📉 ####"
        '> "Time to say good bye"\t\n\nAndrea Bocelli'
    elif list(response_spx['df']["Action"].values())[-1] == 'Sell':
        "#### S&P seems slightly *over*valued. Consider reducing your S&P exposure moderately... 🤔 ####"
        '> "Don\'t cry because it\'s over, smile because it happened."\t\n\nDr Seuss'
    elif list(response_spx['df']["Action"].values())[-1] == 'Buy':
        "#### S&P seems slightly *under*valued. Consider going moderately long your S&P exposure... 🤔 ####"
        '> "You can\'t start a fire without a little spark"\t\n\nBruce Springsteen'
    elif list(response_spx['df']["Action"].values())[-1] == 'Strong Buy':
        "#### S&P seems *under*valued. Consider going long your S&P exposure... 📈 ####"
        '> "You can\'t start a fire without a little spark"\t\n\nBruce Springsteen'
