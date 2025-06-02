import os
from typing import TypedDict, Literal, List, Union
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

# Importer les fonctions de création des graphes des sous-agents
from .generic_chatbot_agent import create_generic_chatbot_graph # GenericChatbotAgentState n'est pas utilisé directement ici
from .incident_analysis_agent import create_incident_analysis_graph # IncidentAnalysisAgentState n'est pas utilisé directement ici

load_dotenv()

# Initialiser le client LangChain avec OpenAI
MODEL_NAME = "gpt-4o-mini"

llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)


# Définir le schéma de sortie pour LangChain
class RouteDecision(BaseModel):
    step: Literal["generic_chatbot", "incident_analysis"] = Field(
        ...,  
        description="Détermine si la demande doit être routée vers 'generic_chatbot' ou 'incident_analysis'."
    )

# Créer le parseur de sortie
output_parser = JsonOutputParser(pydantic_object=RouteDecision)

# 1. Définir l'état de l'orchestrateur
class OrchestratorState(TypedDict):
    question: str
    history: List[dict]  # Pour l'historique de chat
    routing_decision: Literal["generic_chatbot", "incident_analysis"]
    final_response: Union[str, dict]  # Pour stocker la réponse finale
    # Les états des sous-agents pourraient être utiles pour des scénarios plus complexes
    # recipe_agent_state: RecipeAgentState 
    # apartment_agent_state: ApartmentAgentState

# Schéma pour la validation de la sortie structurée du LLM
class Route(BaseModel):
    step: Literal["generic_chatbot", "incident_analysis"] = Field(
        ...,  # Le champ est maintenant obligatoire
        description="Détermine si la demande doit être routée vers 'generic_chatbot' ou 'incident_analysis'."
    )

# Configuration du routeur avec validation de la sortie
router = llm.with_structured_output(Route)


router_prompt = """
Tu es un routeur intelligent pour un système de support IT bancaire. 
Analyse la question et détermine si elle doit être traitée par l'agent de chat générique ou par l'agent d'analyse d'incidents.

Voici les deux possibilités à considérer :

1. Si la question concerne une demande d'analyse d'incident, 
   réponds : "incident_analysis".
   Exemples : 
   - "analyse moi l'incident INC2309845"
   - "Explique moi l'incident INC2309846"
   
2. Pour toutes les autres questions générales, informations, demandes de renseignements ou conversations courantes,
   réponds : "generic_chatbot".
   Exemples :
   - "Bonjour, comment allez-vous ?"
   - "Explique moi le fonctionnement de la voiture électrique"

Ta réponse doit être UNIQUEMENT un des deux mots suivants : "generic_chatbot" ou "incident_analysis".
"""

# 2. Définir les nœuds de l'orchestrateur
def route_question(state: OrchestratorState) -> dict:
    print("---ORCHESTRATEUR: ROUTAGE DE LA QUESTION---")
    question = state["question"]
    
    try:
        print(f"Question à router: {question}")
        decision = router.invoke(
            [
                SystemMessage(content=router_prompt),
                HumanMessage(content=question),
            ]
        )
        print(f"Décision de routage: {decision.step}")
        # Mise à jour de l'état avec la décision de routage
        state["routing_decision"] = decision.step
        return state
        
    except Exception as e:
        print(f"Erreur lors du routage: {str(e)}")
        # Fallback en cas d'échec
        state["routing_decision"] = "generic_chatbot"
    
    return state

def invoke_generic_chatbot_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT CHATBOT GENERIQUE---")
    question = state["question"]
    generic_chatbot_graph = create_generic_chatbot_graph()
    generic_chatbot_input = {"question": question}
    final_agent_state = generic_chatbot_graph.invoke(generic_chatbot_input)
    return {"final_response": final_agent_state.get("response", "Désolé, je n'ai pas pu générer de réponse.")}

def invoke_incident_analysis_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT INCIDENT ANALYSIS---")
    question = state["question"]
    incident_analysis_graph = create_incident_analysis_graph()
    incident_analysis_input = {"question": question}
    final_agent_state = incident_analysis_graph.invoke(incident_analysis_input)
    return {"final_response": final_agent_state.get("response", "Pas d'appartement trouvé.")}

def fallback_node(state: OrchestratorState):
    print("---ORCHESTRATEUR: NŒUD PAR DÉFAUT (FALLBACK)---")
    return {"final_response": "Désolé, je ne peux pas traiter ce type de demande pour le moment. Essayez une recherche de recette ou d'appartement."}

# 3. Définir les arêtes conditionnelles
def decide_next_node(state: OrchestratorState):
    decision = state['routing_decision']
    print(f"---ORCHESTRATEUR: DÉCISION DU PROCHAIN NŒUD basé sur '{decision}'---")
    if decision == "generic_chatbot":
        return "generic_chatbot_agent"
    elif decision == "incident_analysis":
        return "incident_analysis_agent"
    else:
        return "fallback"

# 4. Construire le graphe de l'orchestrateur
def create_orchestrator_graph():
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("router", route_question)
    workflow.add_node("generic_chatbot_agent", invoke_generic_chatbot_agent)
    workflow.add_node("incident_analysis_agent", invoke_incident_analysis_agent)
    workflow.add_node("fallback", fallback_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "generic_chatbot_agent": "generic_chatbot_agent",
            "incident_analysis_agent": "incident_analysis_agent",
            "fallback": "fallback",
        },
    )

    workflow.add_edge("generic_chatbot_agent", END)
    workflow.add_edge("incident_analysis_agent", END)
    workflow.add_edge("fallback", END)
    
    app = workflow.compile()
    return app

