from langgraph.graph import StateGraph
from app.core.state import State
from app.nodes.symptom_parser import parse_symptoms
from app.nodes.check_history import check_history
from app.nodes.predict_condition import predict_condition
from app.nodes.recommend_action import recommend_action
from app.nodes.suggest_doctor import suggest_doctor
from app.nodes.search_doctors_nearby import search_doctors_nearby
from app.nodes.update_history import update_history

builder = StateGraph(State)
builder.add_node("parse_symptoms", parse_symptoms)
builder.add_node("check_history", check_history)
builder.add_node("predict_condition", predict_condition)
builder.add_node("recommend_action", recommend_action)
builder.add_node("suggest_doctor", suggest_doctor)
builder.add_node("search_doctors_nearby", search_doctors_nearby)
builder.add_node("update_history", update_history)

builder.set_entry_point("parse_symptoms")
builder.add_edge("parse_symptoms", "check_history")
builder.add_edge("check_history", "predict_condition")
builder.add_edge("predict_condition", "recommend_action")
builder.add_edge("recommend_action", "suggest_doctor")
builder.add_edge("suggest_doctor", "search_doctors_nearby")
builder.add_edge("search_doctors_nearby", "update_history")
builder.set_finish_point("update_history")

graph = builder.compile()
