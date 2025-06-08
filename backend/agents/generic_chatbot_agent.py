from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Constante pour le nœud de départ
START = None

# 1. Définir l'état de l'agent de chatbot générique
class GenericChatbotAgentState(TypedDict):
    question: str
    response: str
    conversation_context: Dict[str, Any]
    history: List[dict]

# 2. Définir les nœuds de l'agent
def GenericChatbot(state: GenericChatbotAgentState):
    print("---AGENT CHATBOT GENERIQUE---")
    
    # Récupérer le contexte et la question
    context = state.get("conversation_context", {})
    question = state['question']
    
    print(f"[GENERIC CHATBOT] Contexte reçu: {context}")
    print(f"[GENERIC CHATBOT] Question: {question}")
    
    # Dans un vrai scénario, on pourrait utiliser le contexte pour personnaliser la réponse
    response = f"Voici une réponse du Chatbot Générique pour '{question}'"
    
    # Mise à jour du contexte si nécessaire
    # Par exemple, on pourrait suivre le nombre d'interactions
    if "interaction_count" not in context:
        context["interaction_count"] = 1
    else:
        context["interaction_count"] += 1
    
    print(f"[GENERIC CHATBOT] Réponse générée: {response}")
    
    return {
        "response": response,
        "conversation_context": context
    }

# 3. Définir le graphe de l'agent de chatbot générique
def create_generic_chatbot_graph():
    workflow = StateGraph(GenericChatbotAgentState)
    
    # Définir le nœud principal
    workflow.add_node("GenericChatbot", GenericChatbot)
    
    # Définir les transitions
    # Le premier nœud est défini sans source, ce qui en fait le point d'entrée
    workflow.set_entry_point("GenericChatbot")
    workflow.add_edge("GenericChatbot", END)
    
    # Compiler le workflow
    app = workflow.compile()
    
    # Fonction pour initialiser l'état si nécessaire
    def _init_state(state):
        if not state.get("conversation_context"):
            state["conversation_context"] = {}
        if not state.get("history"):
            state["history"] = []
        if not state.get("response"):
            state["response"] = ""
        return state
    
    # Envelopper la fonction invoke pour gérer l'initialisation
    original_invoke = app.invoke
    
    def wrapped_invoke(input_state):
        # Initialiser l'état
        state = _init_state(input_state.copy())
        # Appeler la fonction originale
        return original_invoke(state)
    
    app.invoke = wrapped_invoke
    
    return app
