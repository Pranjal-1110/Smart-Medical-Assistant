from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.state import State
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import json

load_dotenv()

# Use a fast, cheap LLM for this simple parsing task
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class CanonicalSymptoms(BaseModel):
    """Structured output for canonical symptom extraction."""
    symptoms: List[str] = Field(
        description="A list of standardized symptom keywords, always listed in alphabetical order. "
        "Example: If the input includes 'cough and fever', the output must be ['cough', 'fever']. "
        "Normalize synonyms: 'breathlessness' must be standardized to 'shortness of breath'."
    )

prompt = """
You are a highly consistent and standardized medical data parser. Your sole task is to extract key symptoms 
from the user's input and return them as a standardized, alphabetical list.

---
**CRITICAL INSTRUCTIONS FOR STANDARDIZATION:**
1. **Normalization:** Always map common synonyms to a single term. For example:
    * 'difficulty breathing', 'breathlessness' --> **'shortness of breath'**
    * 'nausea', 'upset stomach' --> **'nausea'**
    * 'head pain', 'my head hurts' --> **'headache'**
2. **Alphabetical Order:** The output list must be sorted alphabetically (e.g., ['cough', 'fever'], NOT ['fever', 'cough']).

Here are some examples:
User Input: "I have a cough and a mild fever."
Canonical Symptoms: ["cough", "fever"]

User Input: "Experiencing shortness of breath and chest pain."
Canonical Symptoms: ["chest pain", "shortness of breath"]

User Input: "Feeling nauseous with a headache."
Canonical Symptoms: ["headache", "nausea"]

User Input: "My symptoms include dizziness, fever, and cough."
Canonical Symptoms: ["cough", "dizziness", "fever"]
---

Analyze the following user input and return the canonical symptom list.
"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "User Input: {input}")
])

async def symptom_parser(state: State) -> State:
    raw_symptoms = state.symptoms # The raw user input string
    
    chain = chat_prompt | llm.with_structured_output(CanonicalSymptoms)
    
    # Run the LLM to get the canonical, sorted list
    result = await chain.ainvoke({"input": raw_symptoms})
    
    parsed = result if isinstance(result, CanonicalSymptoms) else CanonicalSymptoms(**result)
    
    # This parsed.symptoms (e.g., ["cough", "fever"]) is the Canonical Key basis!
    return state.model_copy(update={"parsed_symptoms": parsed.symptoms})