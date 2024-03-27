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
