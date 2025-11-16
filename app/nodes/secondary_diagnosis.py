from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from app.services.mongodb import get_patient_history
from dotenv import load_dotenv  

load_dotenv()

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a medical expert that predicts the condition from symptoms and patient history."),
    ("human", "Symptoms: {symptoms}\nHistory: {history}")
])

async def secondary_diagnosis(state: State) -> State:
    history = await get_patient_history(state.patient_id)
    chain = prompt | llm
    response = await chain.ainvoke({
        "symptoms": ", ".join(state.parsed_symptoms),
        "history": history
    })
    return state.model_copy(update={"predicted_condition": str(response.content).strip() , "history": history or {}})