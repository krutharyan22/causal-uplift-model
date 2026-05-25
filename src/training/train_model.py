import pandas as pd
import numpy as np
import joblib
import os

from econml.dml import CausalForestDML

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

print("Loading dataset...")

# Load dataset
df = pd.read_csv("data/raw/hillstrom.csv")

print("\nDataset shape:")
print(df.shape)

print("\nTreatment values:")
print(df["treatment"].unique())

# Convert treatment into binary
# 1 = received email
# 0 = no email

df["treatment_binary"] = (
    df["treatment"] != "No E-Mail"
).astype(int)

print("\nTreatment counts:")
print(df["treatment_binary"].value_counts())

# Outcome variable
Y = df["spend"]

# Treatment variable
T = df["treatment_binary"]

# Feature columns
X = df[[
    "recency",
    "history",
    "mens",
    "womens",
    "newbie"
]]

print("\nFeature sample:")
print(X.head())

# Split dataset
X_train, X_test, T_train, T_test, Y_train, Y_test = train_test_split(
    X,
    T,
    Y,
    test_size=0.2,
    random_state=42
)

print("\nTraining model...")

# Build causal forest model
model = CausalForestDML(

    model_y=RandomForestRegressor(
        n_estimators=48,
        min_samples_leaf=10,
        random_state=42
    ),

    model_t=LogisticRegression(
        max_iter=1000
    ),

    discrete_treatment=True,

    n_estimators=48,
    min_samples_leaf=5,
    random_state=42
)

# Train model
model.fit(
    Y_train,
    T_train,
    X=X_train
)

print("\nModel training complete!")

# Generate uplift predictions
effects = model.effect(X_test)

print("\nSample uplift predictions:")
print(effects[:10])

print("\nAverage uplift:")
print(np.mean(effects))

# Create artifacts folder
os.makedirs("data/artifacts", exist_ok=True)

# Save trained model
joblib.dump(
    model,
    "data/artifacts/causal_model.pkl"
)

print("\nModel saved successfully!")