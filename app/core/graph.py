from langgraph.graph import StateGraph
from app.core.state import State
from app.nodes.primary_daignosis import primary_diagnosis
from app.nodes.secondary_diagnosis import secondary_diagnosis
from app.nodes.recommend_action import recommend_action
from app.nodes.suggest_doctor import suggest_doctor
from app.nodes.search_doctors_nearby import search_doctors_nearby
from app.nodes.update_history import update_history

builder = StateGraph(State)
builder.add_node("primary_diagnosis", primary_diagnosis)
builder.add_node("secondary_diagnosis", secondary_diagnosis)
builder.add_node("recommend_action", recommend_action)
builder.add_node("suggest_doctor", suggest_doctor)  
builder.add_node("search_doctors_nearby", search_doctors_nearby)
builder.add_node("update_history", update_history)

builder.set_entry_point("primary_diagnosis")
builder.add_edge("primary_diagnosis", "secondary_diagnosis")
builder.add_edge("secondary_diagnosis", "recommend_action")
builder.add_edge("recommend_action", "suggest_doctor")
builder.add_edge("suggest_doctor", "search_doctors_nearby")
builder.add_edge("search_doctors_nearby", "update_history")
builder.set_finish_point("update_history")

graph = builder.compile()
