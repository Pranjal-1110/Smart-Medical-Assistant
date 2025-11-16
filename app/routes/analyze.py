from fastapi import APIRouter, Request
from app.core.graph import graph
from app.core.state import State

router = APIRouter(prefix= "/analyze" , tags=["Analyze"])

@router.post("/symptoms")
async def analyze_symptoms(request: Request):
    data = await request.json()
    patient_id = data.get("patient_id")
    symptoms = data.get("symptoms")
    location = data.get("location" , "")

    input_state = State(
        patient_id=patient_id,
        symptoms=symptoms,
        location=location,
        parsed_symptoms=[],
        primary_diagnosis="",
        secondary_diagnosis="",
        history={},
        recommended_action="",
        recommended_doctor="",
        nearby_doctors=[]
    )
    result = await graph.ainvoke(input_state)
    return result
