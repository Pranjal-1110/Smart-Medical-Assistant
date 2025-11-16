from typing import TypedDict, Optional, List
from pydantic import BaseModel

class State(BaseModel):
    patient_id: str
    symptoms: str
    location: str
    parsed_symptoms: List[str]
    primary_diagnosis: str
    history: dict
    secondary_diagnosis: str
    recommended_action: str
    recommended_doctor: str
    nearby_doctors: List[str]
    messages: Optional[List[str]] = []  # For custom messages/notifications