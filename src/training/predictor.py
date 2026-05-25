import pandas as pd
import joblib

print("Loading trained model...")

# Load saved model
model = joblib.load(
    "data/artifacts/causal_model.pkl"
)

print("Model loaded successfully!")

# Example new customer
new_user = pd.DataFrame([{
    "recency": 10,
    "history": 500,
    "mens": 0,
    "womens": 1,
    "newbie": 0
}])

print("\nNew customer:")
print(new_user)

# Predict uplift
uplift = model.effect(new_user)

score = uplift[0]

print("\nPredicted uplift:")
print(score)

# Business decision logic
if score > 2:
    decision = "SEND_COUPON"

elif score > 0:
    decision = "SMALL_DISCOUNT"

else:
    decision = "NO_COUPON"

print("\nDecision:")
print(decision)