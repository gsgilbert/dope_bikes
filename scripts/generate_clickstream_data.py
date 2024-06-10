import json
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Ensure the raw data directory exists
raw_data_dir = os.path.join('data', 'raw')
os.makedirs(raw_data_dir, exist_ok=True)

fake = Faker()

# Generate clickstream data for the past 10 days
for day in range(10):
    clickstream_data = []
    # Determine the date for the current file
    current_date = datetime.now() - timedelta(days=day)
    # Randomly decide the number of records for this day
    num_records = random.randint(1500, 2000)
    
    for _ in range(num_records):
        event = {
            "user_id": fake.uuid4(),
            "timestamp": (current_date - timedelta(seconds=random.randint(0, 86400))).isoformat(),  # 86400 seconds in a day
            "page_url": fake.url(),
            "referrer_url": fake.url(),
            "event_type": random.choice(["page_view", "click", "purchase"]),
            "product_id": random.randint(1, 100) if random.random() > 0.7 else None
        }
        clickstream_data.append(event)

    # Save to a JSON file in the raw data directory
    file_name = f'clickstream_{current_date.strftime("%Y%m%d")}.json'
    file_path = os.path.join(raw_data_dir, file_name)
    with open(file_path, 'w') as f:
        json.dump(clickstream_data, f, indent=4)

    print(f"Generated {num_records} records for {current_date.strftime('%Y-%m-%d')} and saved to {file_path}")
