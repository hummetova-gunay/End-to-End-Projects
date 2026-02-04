# Create POST /predict

# Input:{ 'x' : float}
# Output : {"prediction": float}
# Prediction logic: y = 2x + 1


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
from contextlib import asynccontextmanager
# pydantic model for an input data
class UserInput(BaseModel):
    x: float

app = FastAPI()

@app.post('/predict/')
def predict_output(data: UserInput):
    prediction= 2*data.x + 1
    return {'prediction': prediction}

# -------------------------------------------------------------------

# "features": [1.2, 3.4, 5.6]
# "prediction": 10.2 - sum of features

class InputFeatures(BaseModel):
    features: List[float]

@app.post('/predict-sum/')
def predict_sum(data: InputFeatures):
    prediction = sum(data.features)
    return {'prediction': prediction}

# --------------------------------------------------------------------

# Input: { "x": 4 }
# Prediction: { "prediction": 16 }

class Root(BaseModel):
    x: float

@app.post('/predict-square/')
def square(data: Root):
    return {'prediction': data.x**2}


# ------------------------------------------------------------------------
# endpoint: POST /linear
# input: {
#   "x1": 2.0,
#   "x2": 3.0
# }

# y = 3*x1 + 5*x2 + 2

class TwoFeatures(BaseModel):
    x1: float
    x2: float

@app.post('/linear/')
def linear_model(data:TwoFeatures):
    prediction = 3*data.x1 + 5*data.x2 +2
    return {'prediction': prediction}

# -------------------------------------------------------------------------

# Mean of Features
# endpoint : mean
# input {
#   "features": [1, 2, 3, 4]
# }
# prediction:  { "prediction": 2.5 }

class FeatureVectors(BaseModel):
    vectors: List[float]

@app.post('/mean/')
def predict_mean(data: FeatureVectors):
    prediction = np.mean(data.vectors)
    return {'prediction': prediction}
# ---------------------------------------------------------------------------

# Feature Length Validation
# endpoint: /fixed-model
# Exactly 3 features required
# If not, return error
class InputData(BaseModel):
    features: List[float]

@app.post('/fixed-model/')
def length_check(data: InputData):
    if len(data.features) != 3:
        return {'Error': 'Input features must be 3'}
    return {'Prediction': sum(data.features)}

# ----------------------------------------------------------------------------
# Batch Sum Model
# endpoint : batch-sum
# input :
# {
#   "data": [
#     [1, 2],
#     [3, 4],
#     [5, 6]
#   ]
# }

# prediction :
# {
#   "predictions": [3, 7, 11]
# }

class InputData_2(BaseModel):
    batches: List[List[float]]

@app.post('/batch-sum/')
def batch_sum(data: InputData_2):
    prediction = []
    for batch in data.batches:
        prediction.append(sum(batch)) 
    return {'prediction': prediction}

# Batch Mean Model
# endpoint batch-mean
@app.post('/batch-mean/')
def batch_mean(data:InputData_2):
    prediction = []
    for batch in data.batches:
        prediction.append(np.mean(batch)) 
    return {'prediction': prediction}

# -------------------------------------------------------------------------
# Range Validation
# endpoint: safe-predict
# All features must be between 0 and 100

# Reject invalid input

class InputData_3(BaseModel):
    features: List[float]

@app.post('/safe-predict/')
def safe_predict(data: InputData_3):
    if any(i < 0 or i > 100 for i in data.features):
        raise HTTPException(
        status_code=400,
        detail="All features must be between 0 and 100"
    )
    return {'Prediction': 'Success'}

# Empty Input Handling

# Empty feature list → return error

# Explain error clearly
@app.post('/no-empty/')
def no_features_restriction(data: InputData_3):
    if len(data.features)==0:
        return {'Error': 'Minimum one feature required'}
    return {'Prediction': 'Success'}


# --------------------------------------------------------------------------

# Model Warm-Up
# Use @app.on_event("startup")

# Initialize a fake model variable

# Ensure prediction fails if model not loaded


# Fake model (placeholder)
# -------------------------
def load_fake_model():
    return "model_loaded"

# -------------------------
# Lifespan handler
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.model = load_fake_model()
    print("Model loaded")

    yield

    # Shutdown (optional cleanup)
    print("App shutting down")

app = FastAPI(lifespan=lifespan)

# -------------------------
# Schemas
# -------------------------
class InputFeatures(BaseModel):
    features: List[float]

# -------------------------
# Prediction endpoint
# -------------------------
@app.post("/model-predict/")
def model_predict(data: InputFeatures):
    if not hasattr(app.state, "model"):
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )

    # Fake inference
    prediction = sum(data.features)
    return {"prediction": prediction}