import csv
from sqlalchemy.orm import Session
from pymongo import MongoClient
from app.models import Patient, Base, engine, SessionLocal
import os

# Create tables
Base.metadata.create_all(bind=engine)

# Load CSV
with open('sample_patients.csv') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Insert into Postgres
db: Session = SessionLocal()
for row in data:
    patient = Patient(name=row['name'], age=int(row['age']), diagnosis=row['diagnosis'])
    db.add(patient)
db.commit()

# Insert into MongoDB
client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
mongo_db = client["patients_db"]
reports = mongo_db["reports"]

for i, row in enumerate(data, start=1):
    reports.insert_one({
        "patient_id": i,
        "summary": f"Patient {row['name']} has {row['diagnosis']}"
    })

print("ETL finished.")
