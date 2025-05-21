from app.core.state import State
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')


def search_doctors_nearby(state: State) -> State:
    specialization = state["recommended_doctor"]
    location = state.get("location", "near me")

    query = f"{specialization} doctors near {location}"

    tavily_tool = TavilySearchResults(k=5)

    search_results = tavily_tool.invoke({"query": query})

    # top_doctors = [res['title'] for res in search_results['results'][:5]] if 'results' in search_results else []

    top_doctors = search_results

    return {**state, "nearby_doctors": top_doctors}
