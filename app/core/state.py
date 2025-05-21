from typing import TypedDict, Optional, List

class State(TypedDict):
    patient_id: str
    symptoms: str
    location: str
    parsed_symptoms: str
    history: dict
    predicted_condition: str
    recommended_action: str
    recommended_doctor: str
    nearby_doctors: List[str]