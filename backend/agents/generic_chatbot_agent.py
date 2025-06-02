from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Définir l'état de l'agent de recettes
class GenericChatbotAgentState(TypedDict):
    question: str
    response: str

# 2. Définir les nœuds de l'agent
def GenericChatbot(state: GenericChatbotAgentState):
    print("---AGENT CHATBOT GENERIQUE---")
    question = state['question']
    response = f"Voici une réponse du Chatbot Generique pour '{question}': XXXX"
    print(f"GenericChatbot Reponse: {response}")
    return {"response": response}

# 3. Définir le graphe de l'agent de chatbot generique
def create_generic_chatbot_graph():
    workflow = StateGraph(GenericChatbotAgentState)
    workflow.add_node("GenericChatbot", GenericChatbot)
    workflow.add_edge(START, "GenericChatbot")
    workflow.add_edge("GenericChatbot", END)
    app = workflow.compile()
    return app
