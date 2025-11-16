from app.core.state import State
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv  

load_dotenv()

prompt = """
You are an experienced medical assistant. Based on the recommended action, and the secondary diagnosis provided, suggest the most suitable type of doctor (only the specialization, e.g., 'Cardiologist', 'General Physician', 'Dermatologist').
You can refer to the following examples for guidance:
1.
Recommended Action: "Patient should see a cardiologist for further evaluation and management of heart-related symptoms."
Secondary Diagnosis: "Possible cardiac arrhythmia"
Suggested Doctor: "Cardiologist"

2.
Recommended Action: "Patient should consult a dermatologist for skin rash and irritation."
Secondary Diagnosis: "Dermatitis"
Suggested Doctor: "Dermatologist"

3.
Recommended Action: "Patient should visit a general physician for initial assessment and treatment."
Secondary Diagnosis: "Mild fever and cough"
Suggested Doctor: "General Physician"
"""

llm = ChatOpenAI(model = "gpt-4o-mini" , temperature=0)
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "For the following recommended action, and secondary diagnosis suggest the most suitable type of doctor:\n{recommended_action}\n{secondary_diagnosis}"),
])

async def suggest_doctor(state: State) -> State:
    recommended_action = state.recommended_action
    secondary_diagnosis = state.secondary_diagnosis
    chain = chat_prompt | llm
    response = await chain.ainvoke({
        "recommended_action": recommended_action,
        "secondary_diagnosis": secondary_diagnosis
    })
    doctor_specialization = str(response.content).strip()
    return state.model_copy(update={"recommended_doctor": doctor_specialization})
