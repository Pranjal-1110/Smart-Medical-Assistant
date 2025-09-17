from app.services.mongodb import get_patient_history
from app.core.state import State

async def check_history(state: State) -> State:
    patient_id = state["patient_id"]
    history = await get_patient_history(patient_id)
    return {**state, "history": history or {}}