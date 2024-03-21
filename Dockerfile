FROM python:3.10.6-buster

WORKDIR /prod

COPY btm btm
COPY requirements_prod.txt requirements.txt
COPY test_set.csv test_set.csv
COPY train_set.csv train_set.csv
COPY setup.py setup.py
# COPY setup.py setup.py
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
