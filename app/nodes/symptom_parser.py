from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful medical assistant that extracts key symptoms from the user description. You just need to parse the symptoms, and provide no other mdical advice."),
    ("human", "{input}")
])

def parse_symptoms(state: State) -> State:
    symptoms = state["symptoms"]
    chain = prompt | llm
    parsed = chain.invoke({"input": symptoms})
    return {**state, "parsed_symptoms": str(parsed.content).strip()}