import streamlit as st
import requests
import pandas as pd
from PIL import Image
import pickle
import shap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.markdown("# __Beat the Market__ #")
"__Come to the Data Science side of trading and try to **b**eat **t**he **m**arket with us!__"

"We are using Machine Learning to compute fair values of the S&P 500!"

st.markdown("[Go to computations](Computations)")
st.markdown("[Find out about or methods](Background)")

"### Disclaimer ###"
"""
This application is intended for informational and educational purposes only. The fair values provided for the S&P 500 are based on certain algorithms and methodologies which may not accurately predict market movements or future stock prices. The information provided by this application should not be considered as financial advice or a recommendation to buy, sell, or hold any securities.
"""
"""
Trading and investing in the stock market involves inherent risks, including the risk of loss of capital. The user of this application acknowledges and agrees that they are solely responsible for any investment decisions made based on the information provided by this application. The creator of this application shall not be held liable for any losses, damages, or legal consequences arising from the use of this application or reliance on its content.
"""
"""
Users are advised to conduct their own research, seek professional advice, and exercise caution before making any investment decisions. Past performance is not indicative of future results, and the stock market is subject to various factors and uncertainties that may cause prices to fluctuate unpredictably.
"""
"""
By using this application, the user agrees to release the creator from any and all liability arising from the use of the application or reliance on its content.
"""
