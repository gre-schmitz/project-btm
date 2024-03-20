from fastapi import FastAPI
from pydantic import BaseModel
from project_btm import YourModel

app = FastAPI()

class InputData(BaseModel):
    field1: float
    field2: float

model = YourModel()

@app.post("/predict/")
def predict(input_data: InputData):
    field1 = input_data.field1
    field2 = input_data.field2
    prediction = model.predict(field1, field2)
    return {"prediction": prediction}

@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Make a POST request to /predict/ with input data to get predictions."}
