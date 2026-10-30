from faker import Faker
import json
import random
from datetime import datetime

fake = Faker()

def generate_patient_record():
    """Generate a single patient record with PII."""
    diagnoses = ["Hypertension", "Diabetes", "Asthma", "COVID-19", "Cardiovascular Disease"]
    record = {
        "timestamp": datetime.now().isoformat(),
        "patient_id": str(random.randint(10000000, 99999999)),
        "ssn": fake.ssn(),
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "diagnosis": random.choice(diagnoses),
        "ip_address": fake.ipv4()
    }
    return record

def generate_log_entries(count=50):
    """Generate multiple log entries into healthcare_raw.log."""
    with open("healthcare_raw.log", "w", encoding="utf-8") as f:
        for _ in range(count):
            record = generate_patient_record()
            f.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    generate_log_entries(50)
    print("Generated 50 log entries in healthcare_raw.log")
