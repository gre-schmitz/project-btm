import streamlit as st
import requests
import pandas as pd
from PIL import Image
import pickle
import shap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

url_spx = 'http://localhost:8000/latest_spx_predictions'

response_spx = requests.get(url_spx).json()


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
""
"##### Interpolated Actual vs predicted #####"
image_gdp_actual_predicted = Image.open('images/GDP_actual_vs_predicted.png')
st.image(image_gdp_actual_predicted, use_column_width=True)

"""We have lineally interpolated the GDP between two official announcements and then trained
our model to predict these using more than 60 features!"""

"""Please note, that our model only works around a quarter ahead from today.
If you want to predict within that range, however, we believe we have a powerful
predictor regarding the GDP in real time!"""

"## Predicting the S&P 500 using our real time GDP ##"

"""Having a predictor for the real time GDP.. why don't we use it on the stock
market? Our idea is to calculate **fair values** for today's S&P and other
financial figures to help us find investing strategies."""
""
"##### Basic idea of our webapp #####"
flowchart = Image.open('images/flowchart.png')
st.image(flowchart, use_column_width=True)

"""Again we have used a Machine Learning Model to find the connection of each
feature in our data set to the S&P"""

"""Our backwardly directed training gave our model a pretty good idea:"""
""
"##### Training our S&P model #####"
sp_backwards = Image.open('images/sp_backward.png')
st.image(sp_backwards, use_column_width=True)

######################PLOTLY#############################

df_plot_life = pd.DataFrame(response_spx['df'])
df_plot_life.index = pd.to_datetime(df_plot_life.index)
st.write(df_plot_life.head())

df_plot_life['Market'] = df_plot_life['Market'].astype(float)
df_plot_life['BTM Model'] = df_plot_life['BTM Model'].astype(float)

# Creating a figure with secondary_y axis (two y-axes)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Function to generate hover text including the 'Action'
def create_hover_text(df):
    return [f"{date.strftime('%Y-%m-%d')}<br>Market: {market}<br>BTM Model: {model}<br>Action: {action}"
            for date, market, model, action in zip(df.index, df['Market'], df['BTM Model'], df['Action'])]

# Custom hover text for all data points
hover_text = create_hover_text(df_plot_life)

# Adding Market and BTM Model as line plots with custom hover info
fig.add_trace(
    go.Scatter(x=df_plot_life.index, y=df_plot_life['Market'], name='Market', mode='lines',
               line=dict(color='blue'), text=hover_text, hoverinfo='text'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df_plot_life.index, y=df_plot_life['BTM Model'], name='BTM Model', mode='lines',
               line=dict(color='green'), text=hover_text, hoverinfo='text'),
    secondary_y=False,
)

# Modifying the 'Diff Z-score' bar chart to include 'Action' in hover
fig.add_trace(
    go.Bar(x=df_plot_life.index, y=df_plot_life['Diff Z-score'], name='Signal Strength',
           marker_color='pink', opacity=0.5, width=0.5,
           marker_line_color='pink', marker_line_width=1,
           text=hover_text, hoverinfo='text'),  # Include custom hover info
    secondary_y=True,
)

# # Adding titles and labels
# fig.update_layout(
#     title_text="S&P500 vs BTM Model with Signal Strength",
#     plot_bgcolor='white', paper_bgcolor='white',
#     xaxis=dict(title='Date'),
#     yaxis=dict(title='Value'),
#     yaxis2=dict(title='Signal Strength')
# )

# chatgpt
fig.update_layout(
    title_text="S&P500 vs BTM Model with Signal Strength",
    title_font=dict(color='black'),  # Customize title font color
    plot_bgcolor='white', paper_bgcolor='white',
    xaxis=dict(title='Date', title_font=dict(color='black'), tickfont=dict(color='black'), gridcolor='lightgrey'),  # Customize x-axis font color and grid line color
    yaxis=dict(title='Value', title_font=dict(color='black'), tickfont=dict(color='black'), gridcolor='lightgrey'),  # Customize y-axis font color and grid line color
    yaxis2=dict(title='Signal Strength', title_font=dict(color='black'), tickfont=dict(color='black'), gridcolor='lightgrey'),  # Customize y-axis font color and grid line color
    legend=dict(font=dict(color='black')),  # Customize legend font color
    xaxis_showgrid=True, yaxis_showgrid=True,  # Show grid lines
    xaxis_gridwidth=1, yaxis_gridwidth=1,  # Set grid line width
    xaxis_gridcolor='lightgrey', yaxis_gridcolor='lightgrey'  # Set grid line color
)

st.plotly_chart(fig)





"""Making predictions for the current quarter looks promising (remember we do not
have official GDPs yet, just our live prediction)"""
""
"##### Our S&P model's recent performance #####"
sp_forward = Image.open('images/sp_forward.png')
st.image(sp_forward, use_column_width=True)

"""What can we conclude now from this? We believe that our model's *predicted*
values for the S&P 500 can serve as a *fair value* of the S&P! If our model
is calculating a *lower* value than the actual price of the S&P, this is a buy
signal and vice versa! And also, if they are sufficiently alike... it is time
to grab a cold drink and do nothing."""




"## Calculate fair values ##"

"Ready to get your hands dirty? Let's see today's signals!"
""
"(This might take a minute, things are actually being calculated...)"

#############################################################################
### waterfall ###############################################################
#############################################################################
Target = 'SPX Index '
Drop = ['Quarter being forecasted', 'Advance Estimate From BEA',
        'Publication Date of Advance Estimate','Days until advance estimate',
        'Forecast Error', 'Data releases', 'NDX Index ', 'SPX Index ']

test = pd.read_csv('predict_set_w_btm.csv', index_col='Dates', parse_dates=True) #date_parser=dateparse)
X_test = test.drop(columns=Drop)
y_test = test[Target]

model = pickle.load(open('spx_final_pickle.pkl',"rb"))

explainer = shap.Explainer(model.predict, X_test)
shap_values = explainer(X_test)
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
    f"Based on our calculations from {list(response_spx['df']['BTM GDP'].keys())[-1][:10]} we provide the following signal"

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
        '> "\'Cos opportunity comes once in a lifetime"\t\n\nBruce Springsteen'


    "## What is driving our predictions? ##"

    """It can be spooky to be told stories by Machine Learning algorithms. Let us
    explain what is driving our predictions"""
    ""
#if st.button('find out about our drivers'):
    # print is visible in the server output, not in the page
    #print('button clicked!')
    "##### Our prediction's main drivers #####"
    st.pyplot(shap.plots.waterfall(shap_values[-1]))

    """**Explanation:** The listed features from above tell you wether they have driven
    the S&P's fair value up (red arrows) or down (blue arrows) compared to last year's
    average value of the actual S&P."""
