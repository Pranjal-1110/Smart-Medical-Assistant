from app.services.mongodb import update_patient_history
from app.core.state import State

async def update_history(state: State) -> State:
    patient_id = state["patient_id"]
    entry = {
        "parsed_symptoms": state["parsed_symptoms"],
        "predicted_condition": state["predicted_condition"],
        "recommended_action": state["recommended_action"],
        "recommended_doctor": state["recommended_doctor"]
    }
    await update_patient_history(patient_id, entry)
    return state