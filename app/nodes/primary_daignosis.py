from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

class ParsedSymptoms(BaseModel):
    symptoms: List[str]
    primary_diagnosis: str

prompt =  """ You are a helpful medical assistant that extracts key symptoms from the user description. You need to parse the symptoms, and return a list of the same. You are to only provide the symptoms.

After extracting the symptoms, you are to provide a primary diagnosis based on the symptoms provided. The primary diagnosis should be a brief description of what could be the possible ailment based on the symptoms provided. Remember to keep the primary diagnosis brief and to the point, and based only on the symptoms provided.

You can refer to the following examples:

User Input: "I have been experiencing a severe headache and occasional dizziness."
Parsed Symptoms: ["headache", "dizziness"]
Primary Diagnosis: "Possible migraine or tension headache."

User Input: "My throat is sore, and I have a mild fever."
Parsed Symptoms: ["sore throat", "mild fever"]
Primary Diagnosis: "Possible viral pharyngitis."

User Input: "Lately, I've had a persistent cough and shortness of breath."
Parsed Symptoms: ["persistent cough", "shortness of breath"]
Primary Diagnosis: "Possible asthma exacerbation or bronchitis."
"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "{input}")
])

async def primary_diagnosis(state: State) -> State:
    symptoms = state.symptoms
    chain = chat_prompt | llm.with_structured_output(ParsedSymptoms)
    result = await chain.ainvoke({"input": symptoms})
    parsed = result if isinstance(result, ParsedSymptoms) else ParsedSymptoms(**result)
    parsed.symptoms = sorted(parsed.symptoms)  # Sort symptoms alphabetically

    return state.model_copy(update={"parsed_symptoms": parsed.symptoms, "primary_diagnosis": parsed.primary_diagnosis})