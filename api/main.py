from fastapi import FastAPI
from pydantic import BaseModel

# Import your model from the GitHub repository
from project_btm import YourModel

# Create an instance of the FastAPI class
app = FastAPI()

# Define a request body model using Pydantic
class InputData(BaseModel):
    # Define fields for your input data model
    field1: float
    field2: float

# Initialize your model
model = YourModel()

# Define a route to accept POST requests with input data
@app.post("/predict/")
def predict(input_data: InputData):
    # Extract input data from the request body
    field1 = input_data.field1
    field2 = input_data.field2

    # Make predictions using your model
    prediction = model.predict(field1, field2)

    # Return the prediction
    return {"prediction": prediction}

# Define a route for the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Make a POST request to /predict/ with input data to get predictions."}
