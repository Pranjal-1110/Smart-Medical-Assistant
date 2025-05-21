from app.core.state import State
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv  

load_dotenv()

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced medical assistant. Based on the recommended action provided, suggest the most suitable type of doctor (only the specialization, e.g., 'Cardiologist', 'General Physician', 'Dermatologist')."),
    ("human", "{input}")
])

def suggest_doctor(state: State) -> State:
    recommended_action = state["recommended_action"]
    
    chain = prompt | llm
    response = chain.invoke({"input": recommended_action})
    
    doctor_specialization = str(response.content).strip()

    return {**state, "recommended_doctor": doctor_specialization}
