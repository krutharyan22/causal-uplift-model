from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

# Create FastAPI app
app = FastAPI()

print("Loading trained causal model...")

# Load saved model
model = joblib.load(
    "data/artifacts/causal_model.pkl"
)

print("Model loaded successfully!")

# Input schema
class CustomerFeatures(BaseModel):

    recency: int
    history: float
    mens: int
    womens: int
    newbie: int


# Root endpoint
@app.get("/")
def home():

    return {
        "message": "Causal Uplift API is running!"
    }


# Prediction endpoint
@app.post("/predict")
def predict(customer: CustomerFeatures):

    # Convert request into dataframe
    user_df = pd.DataFrame([{
        "recency": customer.recency,
        "history": customer.history,
        "mens": customer.mens,
        "womens": customer.womens,
        "newbie": customer.newbie
    }])

    # Predict uplift
    uplift = model.effect(user_df)

    score = float(uplift[0])

    # Business policy
    if score > 0.2:
        decision = "SEND_COUPON"

    elif score > 0:
        decision = "SMALL_DISCOUNT"

    else:
        decision = "NO_COUPON"

    return {
        "uplift_score": round(score, 4),
        "decision": decision
    }