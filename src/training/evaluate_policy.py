import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split

print("Loading dataset...")

# Load dataset
df = pd.read_csv("data/raw/hillstrom.csv")

# Binary treatment
df["treatment_binary"] = (
    df["treatment"] != "No E-Mail"
).astype(int)

# Features
X = df[[
    "recency",
    "history",
    "mens",
    "womens",
    "newbie"
]]

# Outcome
Y = df["spend"]

# Treatment
T = df["treatment_binary"]

# Same train/test split
X_train, X_test, T_train, T_test, Y_train, Y_test = train_test_split(
    X,
    T,
    Y,
    test_size=0.2,
    random_state=42
)

print("Loading trained model...")

# Load saved model
model = joblib.load(
    "data/artifacts/causal_model.pkl"
)

# Predict uplift
uplift_scores = model.effect(X_test)

# Create evaluation dataframe
results = X_test.copy()

results["actual_spend"] = Y_test.values
results["treatment"] = T_test.values
results["uplift_score"] = uplift_scores

print("\nTop uplift users:")
print(
    results.sort_values(
        by="uplift_score",
        ascending=False
    ).head(10)
)

# POLICY:
# send coupon only if uplift > threshold

THRESHOLD = 0.2

results["send_coupon"] = (
    results["uplift_score"] > THRESHOLD
).astype(int)

# Simulated metrics

coupon_cost = 1.0

# Estimated revenue from targeted users
targeted_revenue = results[
    results["send_coupon"] == 1
]["actual_spend"].sum()

# Coupon spend
coupon_total_cost = (
    results["send_coupon"].sum()
    * coupon_cost
)

# Net value
net_value = (
    targeted_revenue
    - coupon_total_cost
)

print("\n========== POLICY RESULTS ==========")

print(f"\nUsers receiving coupon: {results['send_coupon'].sum()}")

print(f"\nTotal revenue from targeted users: {targeted_revenue:.2f}")

print(f"\nCoupon cost: {coupon_total_cost:.2f}")

print(f"\nEstimated net value: {net_value:.2f}")