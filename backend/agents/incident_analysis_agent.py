from typing import TypedDict, List
from langgraph.graph import StateGraph, END, START

# 1. Définir l'état de l'agent d'analyse d'incident
class IncidentAnalysisAgentState(TypedDict):
    question: str
    response: str
    conversation_context: dict  # Pour maintenir le contexte de conversation
    history: List[dict]  # Historique de la conversation
    end_conversation: bool  # Indique si la conversation est terminée

# 2. Définir les nœuds de l'agent
def incident_analysis(state: IncidentAnalysisAgentState):
    print("---AGENT INCIDENT ANALYSIS---")
    
    # Récupérer le contexte existant ou en créer un nouveau
    context = state.get("conversation_context", {})
    question = state['question']
    
    print(f"[AGENT] Contexte reçu: {context}")
    
    # Vérifier si c'est une nouvelle conversation
    if not context.get("incident_id"):
        # Extraire l'ID d'incident de la question (exemple simple)
        incident_id = "INC" + "".join(filter(str.isdigit, question)) or "UNKNOWN"
        context["incident_id"] = incident_id
        context["conversation_count"] = 1  # Commencer à 1 pour cette conversation
        
        # Réponse initiale
        response = f"🔍 Analyse de l'incident {incident_id} démarrée. Posez-moi des questions spécifiques ou dites 'fin' pour terminer."
    else:
        # Incrémenter le compteur de conversation
        context["conversation_count"] = context.get("conversation_count", 0) + 1
        
        # Vérifier si l'utilisateur veut terminer
        if any(mot in question.lower() for mot in ["fin", "terminer", "au revoir"]):
            response = f"✅ Fin de l'analyse de l'incident {context['incident_id']}. Retour au menu principal."
            context["end_conversation"] = True
        else:
            # Simuler une réponse à la question de suivi
            response = f"📌 Suite à votre question sur l'incident {context['incident_id']} : Voici les détails demandés pour '{question}'."
    
    # Préparer la réponse finale
    response_data = {
        "response": response,
        "conversation_context": context,
        "end_conversation": context.get("end_conversation", False)
    }
    
    # Log détaillé pour le débogage
    print("\n--- INCIDENT ANALYSIS AGENT DEBUG ---")
    print(f"Question reçue: {question}")
    print(f"Contexte actuel: {context}")
    print(f"Réponse générée: {response}")
    print(f"Fin de conversation: {response_data['end_conversation']}")
    print("--- FIN DU DEBUG ---\n")
    
    return response_data

# 3. Définir le graphe de l'agent incident analysis
def create_incident_analysis_graph():
    workflow = StateGraph(IncidentAnalysisAgentState)
    
    # Définir le nœud d'analyse d'incident
    workflow.add_node("incident_analysis", incident_analysis)
    
    # Définir les transitions
    workflow.add_edge(START, "incident_analysis")
    workflow.add_edge("incident_analysis", END)
    
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
        if "end_conversation" not in state:
            state["end_conversation"] = False
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
