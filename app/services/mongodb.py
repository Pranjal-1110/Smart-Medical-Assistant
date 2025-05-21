from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.smart_medical_db
patients = db.patient_data

def get_patient_history(patient_id: str):
    record = patients.find_one({"patient_id": patient_id})
    return record.get("history") if record else {}

def update_patient_history(patient_id: str, new_data: dict):
    patients.update_one(
        {"patient_id": patient_id},
        {"$push": {"history": new_data}},
        upsert=True
    )