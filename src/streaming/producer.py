from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "customer-events"

print("Starting producer...")

while True:

    customer = {
        "recency": random.randint(1, 10),
        "history": random.randint(50, 3000),
        "mens": random.randint(0, 1),
        "womens": random.randint(0, 1),
        "newbie": random.randint(0, 1)
    }

    producer.send(TOPIC, customer)

    print(f"Produced event: {customer}")

    time.sleep(2)