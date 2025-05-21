from fastapi import APIRouter, Request
from app.core.graph import graph
from app.core.state import State

router = APIRouter()

@router.post("/analyze")
async def analyze_symptoms(request: Request):
    data = await request.json()
    patient_id = data.get("patient_id")
    symptoms = data.get("symptoms")
    location = data.get("location" , "")

    input_state = {
        "patient_id": patient_id,
        "symptoms": symptoms,
        "location": location
    }
    result = graph.invoke(input_state)
    return result
