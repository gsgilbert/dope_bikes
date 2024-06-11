import json
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# Construct the path to the raw data directory
raw_data_dir = script_dir.parent / 'data' / 'raw'
raw_data_dir.mkdir(parents=True, exist_ok=True)

fake = Faker()

# Subpages for the dopebikes.com website
subpages = [
    "home", "products", "products/bike-1", "products/bike-2", "products/bike-3",
    "cart", "checkout", "search", "contact"
]

# Generate clickstream data for the current day
clickstream_data = []
# Determine the date for the current file
current_date = datetime.now()
# Randomly decide the number of records for this day
num_records = random.randint(1500, 2000)

for _ in range(num_records):
    session_id = fake.uuid4()
    user_id = fake.uuid4()
    product_id = random.randint(1, 100) if random.random() > 0.7 else None
    quantity = random.randint(1, 5) if product_id and random.random() > 0.5 else None
    event_type = random.choice(["page_view", "click", "search", "add_to_cart", "purchase"])
    
    event = {
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": (current_date - timedelta(seconds=random.randint(0, 86400))).isoformat(),
        "page_url": f"https://dopebikes.com/{random.choice(subpages)}",
        "referrer_url": f"https://dopebikes.com/{random.choice(subpages)}" if random.random() > 0.5 else fake.url(),
        "event_type": event_type,
        "product_id": product_id,
        "quantity": quantity
    }
    
    # Adjust data for specific event types
    if event_type == "search":
        event["search_query"] = fake.word()
    elif event_type == "add_to_cart":
        event["quantity"] = quantity
    elif event_type == "purchase":
        event["order_id"] = fake.uuid4()
        event["price"] = round(random.uniform(100, 2000), 2)
    
    # Remove keys with None values
    event = {k: v for k, v in event.items() if v is not None}

    clickstream_data.append(event)

# Save to a JSON file in the raw data directory
file_name = f'clickstream_{current_date.strftime("%Y%m%d")}.json'
file_path = raw_data_dir / file_name
with open(file_path, 'w') as f:
    json.dump(clickstream_data, f, indent=4)

print(f"Generated {num_records} records for {current_date.strftime('%Y-%m-%d')} and saved to {file_path}")
