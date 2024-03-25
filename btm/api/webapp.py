import streamlit as st
import requests
import pandas as pd

st.write('hello 👋')



url_spx = 'https://btm-4yiq46myaq-ew.a.run.app/latest_spx_predictions'
url_gdp = 'https://btm-4yiq46myaq-ew.a.run.app/latest_gdp_predictions'

response_spx = requests.get(url_spx).json()
response_gdp = requests.get(url_gdp).json()

# print(list(response_gdp['predictions'].values())[-1])

@st.cache_resource
def get_dataframe_data():
    spx_value = list(response_spx['predictions'].values())[-1]
    gdp_value = list(response_gdp['predictions'].values())[-1]
    index_value = list(response_spx['predictions'].keys())[-1]

    return pd.DataFrame(
        [[spx_value, gdp_value]],
        index=[index_value],
        columns=['S&P 500 fair value', 'GDP real time prediction']
    )

df = get_dataframe_data()


if st.button('get latest computations'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    st.write(df)
