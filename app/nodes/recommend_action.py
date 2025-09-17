from app.core.state import State
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
llm2 = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a doctor, who specializes in being the first point of contact for most of the patients. Based on the predicted condition of the patient, recommend a plan of action in brief."),
    ("human", " Predicted conditions are\n{predicted_condition} \n Previous history is - \n{history}")
])

async def recommend_action(state: State) -> State:
    chain = prompt | llm2
    predicted_condition = state["predicted_condition"].lower()
    response = await chain.ainvoke({"predicted_condition": predicted_condition , 'history': state["history"]})
    return {**state, "recommended_action": str(response.content)}
