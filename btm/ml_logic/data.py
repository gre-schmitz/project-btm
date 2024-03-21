import pandas as pd

from btm.params import *
from google.cloud import bigquery


def load_data():
    '''
    Loads the csv into a DataFrame
    '''
    gdpnow = pd.read_csv('train_set.csv', index_col='Dates', parse_dates=True)
    gdpnow.index = pd.to_datetime(gdpnow.index)
    return gdpnow


# def load_unprocecced_to_bq(
#         gcp_project:str,
#         bq_dataset:str,
#         table:str,
#         write_mode:str
#     ):
#     """
#     - !!! NOT FINISHED !!!
#     - Uploads the yet to be processed DataFrame to BigQuery
#     - DataFrame already should contain the HF-Data
#     """

#     df = pd.read_csv('gdpnow_hf.csv', index_col='Dates', parse_dates=True)
#     df['Change in inventory investment'] = \
#         df['Change in inventory investment ($Bil 2009)']
#     df = df.drop(columns=['Change in inventory investment ($Bil 2009)'])

#     # Table's name in BQ
#     full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
#     print(f"\n Saving data will be done to BigQuery @ {full_table_name}...:")

#     # instantiating BigQuery
#     client = bigquery.Client()

#     # Tell BigQuery if we want to append or truncate
#     job_config = bigquery.LoadJobConfig(write_disposition=write_mode)
#     if write_mode == "WRITE_TRUNCATE":
#         print("\nℹ️: Data will be truncated! Thus, old date will be replaced")
#     elif write_mode == "WRITE_APPEND":
#         print("\nℹ️: Data will be appended to old existing data!")

#     # Upload data
#     job = client.load_table_from_dataframe(df, full_table_name, job_config=job_config)
#     result = job.result()  # wait for the job to complete

#     print(f"✅ Data saved to bigquery, with shape {df.shape}")
