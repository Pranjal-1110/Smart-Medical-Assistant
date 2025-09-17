from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from dotenv import load_dotenv  

load_dotenv()

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a medical expert that predicts the condition from symptoms and patient history."),
    ("human", "Symptoms: {symptoms}\nHistory: {history}")
])

async def predict_condition(state: State) -> State:
    chain = prompt | llm
    response = await chain.ainvoke({
        "symptoms": state["parsed_symptoms"],
        "history": state.get("history", {})
    })
    return {**state, "predicted_condition": str(response.content).strip()}