FROM python:3.10.6-buster

WORKDIR /prod

COPY btm btm
COPY images images
COPY requirements_prod.txt requirements.txt
COPY predict_set.csv predict_set.csv
COPY total_df_w_btm.csv total_df_w_btm.csv
# COPY train_set.csv train_set.csv
COPY predict_set_w_btm.csv predict_set_w_btm.csv
COPY Final_GDP_Interp.pkl Final_GDP_Interp.pkl
COPY spx_final_pickle.pkl spx_final_pickle.pkl
COPY setup.py setup.py

# reads the requirements as to check for needed libraries

RUN pip install --upgrade pip
RUN pip install .
# just as known, this installs the requirements

# make use of the local caching mechanism we put in place for CSVs and Models
COPY Makefile Makefile
# RUN make reset_local_files

CMD uvicorn btm.api.fast:app --host 0.0.0.0 --port $PORT
# launches the univorn server, app = FastAPI() is defined in the 'api' folder
# --host 0.0.0.0 is the local machine
# $PORT is a default value for the google environment for them to select
