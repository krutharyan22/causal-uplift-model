from kafka import KafkaConsumer
import json
import pandas as pd
import joblib

print("Loading model...")

model = joblib.load(
    "data/artifacts/causal_model.pkl"
)

consumer = KafkaConsumer(
    "customer-events",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer started...")

for message in consumer:

    customer = message.value

    print("\nReceived customer:")
    print(customer)

    X = pd.DataFrame([customer])

    uplift = model.effect(X)[0]

    if uplift > 2:
        decision = "SEND_COUPON"
    else:
        decision = "NO_COUPON"

    print(f"Predicted uplift: {uplift:.2f}")
    print(f"Decision: {decision}")