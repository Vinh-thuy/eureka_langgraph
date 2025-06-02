from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Définir l'état de l'agent d'analyse d'incident
class IncidentAnalysisAgentState(TypedDict):
    question: str
    response: str  # Même nom de champ que dans GenericChatbotAgentState

# 2. Définir les nœuds de l'agent
def incident_analysis(state: IncidentAnalysisAgentState):
    print("---AGENT INCIDENT ANALYSIS---")
    question = state['question']
    response = f"Voici le résultat de l'analyse de l'incident pour '{question}': XXXX"
    print(f"IncidentAnalysisAgent Reponse: {response}")
    return {"response": response}

# 3. Définir le graphe de l'agent incident analysis
def create_incident_analysis_graph():
    workflow = StateGraph(IncidentAnalysisAgentState)
    workflow.add_node("incident_analysis", incident_analysis)
    workflow.add_edge(START, "incident_analysis")
    workflow.add_edge("incident_analysis", END)
    app = workflow.compile()
    return app
