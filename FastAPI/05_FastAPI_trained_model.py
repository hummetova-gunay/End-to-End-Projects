# Task 3: Load a Trained Model

# Goal: Production pattern.

# Requirements

# Train a simple sklearn model (linear regression)

# Save using joblib

# Load model once at startup

# Use it inside /predict

# Concepts

# Startup events

# Model persistence

from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import numpy as np


# -------- Lifespan Handler --------
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Startup logic
    app.state.model = joblib.load("model/model.joblib")
    print("Model loaded successfully")

    yield  # App runs here

    # Shutdown logic (optional)
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


# -------- Request Schema --------
class PredictionInput(BaseModel):
    features: list[float]


# -------- Prediction Endpoint --------
@app.post("/predict")
def predict(data: PredictionInput):

    features_array = np.array(data.features).reshape(1, -1)

    prediction = app.state.model.predict(features_array)

    return {"prediction": prediction.tolist()}

# ------------------------------------------------------------------------------------------------

# Task 4: Feature Validation

# Goal: Prevent garbage inputs.

# Requirements

# Ensure:

# Correct number of features

# No NaNs

# Values within allowed range

# Concepts

# Pydantic validators

# Defensive ML serving