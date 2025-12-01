from app.core.state import State
from app.services.models import SearchOutput, DoctorResult
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from app.services.redis_client import get_redis_client, get_cache_key # NEW IMPORTS
import json
import os

load_dotenv()

CACHE_TTL = 86400 # 24 hours TTL for doctor info

async def search_doctors_nearby(state: State) -> State:
    redis_client = await get_redis_client()
    specialization = state.recommended_doctor or "general physician"
    location = state.location
    
    if location is None or location.strip() == "":
        return state.model_copy(update={
            "nearby_doctors": [],
            "messages": ["Please provide your location to get doctor recommendations near you."]
        })
    
    # 1. Generate Canonical Cache Key: Uses specialization and location
    cache_key_parts = [specialization, location]
    cache_key = f"doctor_search:{get_cache_key(cache_key_parts)}"
    
    # 2. Check Cache (Cache-Aside Pattern)
    cached_result_json = await redis_client.get(cache_key)
    
    if cached_result_json:
        print(f"INFO: Cache HIT for {cache_key}")
        # Deserialize JSON string back into the expected list structure
        nearby_doctors_model = SearchOutput.model_validate_json(cached_result_json)
        return state.model_copy(update={"nearby_doctors": nearby_doctors_model.results})

    # 3. Cache Miss: Call Agent & APIs
    print(f"INFO: Cache MISS for {cache_key}. Calling Tavily Agent.")
    query = f"Search for {specialization} doctors near {location}. Extract doctor names, phone numbers, addresses, and any available profile links."
    
    # Use base LLM for the agent
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic = "health",
    )

    # system prompt for the agent
    system_prompt = """You are a helpful medical search assistant specialized in finding healthcare providers.
    Your task is to search for doctors and extract the following information:
    - Doctor's name (mandatory)
    - Phone number (optional) 
    - Address/clinic location (mandatory)
    - Profile links or clinic websites (optional)

    INSTRUCTIONS:
    1. Always provide name, phone number, and address for each doctor found
    2. Use the search tool to get the most relevant and recent information
    3. Focus on licensed medical professionals and established clinics
    4. If multiple doctors are found, prioritize those with complete contact information
    5. Present information in a clear, organized manner

    Remember: Accuracy is crucial when dealing with medical information."""

    agent = create_react_agent(
        llm, [tavily_search_tool], system_prompt=system_prompt
    )
    
    search_results = await agent.ainvoke({"messages": [("user", query)]})
    final_message = search_results["messages"][-1].content
    
   
   # parsing prompt to get structured doctor info
    parsing_prompt = f"""
    Based on the following search results about {specialization} near {location}, extract structured information:
    
    Search Results:
    {final_message}

    You are to extract doctor information including names, phone numbers, and addresses. If profile links are available, extract them as well.
    
    """
    
    structured_llm = llm.with_structured_output(SearchOutput)
    
    try:
        structured_results = await structured_llm.ainvoke(parsing_prompt)
        # Handle the structured output properly
        if isinstance(structured_results, SearchOutput):
            top_doctors = structured_results.results
        else:
            # If it returns a dict, create SearchOutput instance
            top_doctors = SearchOutput(**structured_results).results
    except Exception as e:
        print(f"Error parsing structured output: {e}")
        top_doctors = []

    # 4. Store Result in Cache
    cacheable_output = SearchOutput(results=top_doctors)
    # Store the entire SearchOutput model as a JSON string with TTL
    await redis_client.set(cache_key, cacheable_output.model_dump_json(), ex=CACHE_TTL) 

    return state.model_copy(update={
        "nearby_doctors": top_doctors,
        "messages" : ["Could not parse doctor information from search results."] if not top_doctors else []
    })