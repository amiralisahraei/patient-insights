from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from starlette_graphene3 import GraphQLApp
from app.graphql_schema import schema
import os
from app.models import SessionLocal, Patient, Base, engine


from contextlib import asynccontextmanager
# ...existing imports...

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# ...rest of your code...
db_session = SessionLocal()
mongo_client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
mongo_db = mongo_client["patients_db"]
reports = mongo_db["reports"]

@app.get("/patients")
def get_patients():
    return db_session.query(Patient).all()

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/{patient_id}/report")
def get_patient_report(patient_id: int):
    report = reports.find_one({"patient_id": patient_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"summary": report["summary"]}

@app.get("/metrics")
def metrics():
    return {"api_status": "healthy", "total_patients": db_session.query(Patient).count()}

app.add_route("/graphql", GraphQLApp(schema=schema))
