from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from app.services.redis_client import get_redis_client, get_cache_key 

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini") 

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a medical expert that predicts the most likely condition based ONLY on the standardized symptoms provided. Provide only the name of the most likely condition."),
    ("human", "Standardized Symptoms (ALREADY PARSED): {symptoms}")
])

CACHE_TTL = 3600

class PrimaryDiagnosisOutput(BaseModel):
    primary_diagnosis: str = Field(description="The general, non-personalized primary diagnosis.")

async def primary_diagnosis(state: State) -> State:
    redis_client = await get_redis_client()
    symptoms_list = state.parsed_symptoms
    symptoms_str = ", ".join(symptoms_list)
    
    cache_key = f"primary_analysis:{get_cache_key(symptoms_list)}"
    
    cached_result = await redis_client.get(cache_key)
    
    if cached_result:
        print(f"INFO: Cache HIT for {cache_key}")
        return state.model_copy(update={"primary_diagnosis": cached_result})

    print(f"INFO: Cache MISS for {cache_key}. Calling AI.")
    chain = prompt | llm
    
    response = await chain.ainvoke({"symptoms": symptoms_str})
    result = str(response.content).strip()
    
    await redis_client.set(cache_key, result, ex=CACHE_TTL)

    return state.model_copy(update={"primary_diagnosis": result})