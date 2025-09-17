from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["smart_medical_assistant"]
users_collection = db["users"]
patients_collection = db["patient_data"]
doctor_licenses_collection = db["doctor_licenses"]

# Dummy data for a real-world scenario
async def initialize_doctor_licenses():
    dummy_licenses = [
        {"license_number": "DOC-12345", "email": "doctor1@example.com"},
        {"license_number": "DOC-67890", "email": "doctor2@example.com"}
    ]
    if await doctor_licenses_collection.count_documents({}) == 0:
        await doctor_licenses_collection.insert_many(dummy_licenses)

async def get_patient_history(patient_id: str):
    record = await patients_collection.find_one({"patient_id": patient_id})
    return record.get("history") if record else {}

async def update_patient_history(patient_id: str, new_data: dict):
    await patients_collection.update_one(
        {"patient_id": patient_id},
        {"$push": {"history": new_data}},
        upsert=True
    )