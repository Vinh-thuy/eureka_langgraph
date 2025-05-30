import os
from typing import TypedDict, Literal, List, Union
from langgraph.graph import StateGraph, END # START n'est plus explicitement nécessaire avec set_entry_point
from openai import OpenAI
from dotenv import load_dotenv

# Importer les fonctions de création des graphes des sous-agents
from .recipe_agent import create_recipe_graph # RecipeAgentState n'est pas utilisé directement ici
from .apartment_agent import create_apartment_graph # ApartmentAgentState n'est pas utilisé directement ici

load_dotenv()

# Initialiser le client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"

# 1. Définir l'état de l'orchestrateur
class OrchestratorState(TypedDict):
    question: str
    history: List[dict]  # Pour l'historique de chat si besoin plus tard
    routing_decision: Literal["recette", "appartement", "autre"]
    final_response: Union[str, dict] # Pour stocker la réponse finale
    # Les états des sous-agents pourraient être utiles pour des scénarios plus complexes
    # recipe_agent_state: RecipeAgentState 
    # apartment_agent_state: ApartmentAgentState

# 2. Définir les nœuds de l'orchestrateur
def route_question(state: OrchestratorState):
    print("---ORCHESTRATEUR: ROUTAGE DE LA QUESTION---")
    question = state["question"]
    
    prompt = f"""Vous êtes un assistant IA chargé de router les questions des utilisateurs vers l'agent approprié.
Analysez la question suivante et déterminez si elle concerne une recherche de recette de cuisine, une recherche d'appartement, ou autre chose.
Répondez uniquement par "recette", "appartement", ou "autre".

Question: "{question}"
Classification:"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        decision = response.choices[0].message.content.strip().lower()
        if decision not in ["recette", "appartement", "autre"]:
            print(f"Décision inattendue de l'LLM: '{decision}', utilisation de 'autre' par défaut.")
            decision = "autre"
        print(f"Décision de routage: {decision}")
        return {"routing_decision": decision}
    except Exception as e:
        print(f"Erreur lors du routage LLM: {e}")
        return {"routing_decision": "autre", "final_response": "Désolé, une erreur est survenue lors du routage de votre demande."}

def invoke_recipe_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT RECETTES---")
    question = state["question"]
    recipe_graph = create_recipe_graph()
    recipe_input = {"question": question}
    final_agent_state = recipe_graph.invoke(recipe_input)
    return {"final_response": final_agent_state.get("recipe_details", "Pas de recette trouvée.")}

def invoke_apartment_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT APPARTEMENTS---")
    question = state["question"]
    apartment_graph = create_apartment_graph()
    apartment_input = {"question": question}
    final_agent_state = apartment_graph.invoke(apartment_input)
    return {"final_response": final_agent_state.get("apartment_listing", "Pas d'appartement trouvé.")}

def fallback_node(state: OrchestratorState):
    print("---ORCHESTRATEUR: NŒUD PAR DÉFAUT (FALLBACK)---")
    return {"final_response": "Désolé, je ne peux pas traiter ce type de demande pour le moment. Essayez une recherche de recette ou d'appartement."}

# 3. Définir les arêtes conditionnelles
def decide_next_node(state: OrchestratorState):
    decision = state['routing_decision']
    print(f"---ORCHESTRATEUR: DÉCISION DU PROCHAIN NŒUD basé sur '{decision}'---")
    if decision == "recette":
        return "recipe_agent"
    elif decision == "appartement":
        return "apartment_agent"
    else:
        return "fallback"

# 4. Construire le graphe de l'orchestrateur
def create_orchestrator_graph():
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("router", route_question)
    workflow.add_node("recipe_agent", invoke_recipe_agent)
    workflow.add_node("apartment_agent", invoke_apartment_agent)
    workflow.add_node("fallback", fallback_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "recipe_agent": "recipe_agent",
            "apartment_agent": "apartment_agent",
            "fallback": "fallback",
        },
    )

    workflow.add_edge("recipe_agent", END)
    workflow.add_edge("apartment_agent", END)
    workflow.add_edge("fallback", END)
    
    app = workflow.compile()
    return app

if __name__ == "__main__":
    orchestrator_app = create_orchestrator_graph()

    test_queries = [
        {"question": "Comment faire des crêpes ?", "history": []},
        {"question": "Je cherche un T2 à Lyon", "history": []},
        {"question": "Quelle heure est-il ?", "history": []}
    ]

    for i, inputs in enumerate(test_queries):
        print(f"\n--- TEST ORCHESTRATEUR {i+1}: '{inputs['question']}' ---")
        # Utiliser stream avec stream_mode='values' pour voir l'état complet à chaque étape
        for event in orchestrator_app.stream(inputs, stream_mode="values"):
            print(f"  Événement Orchestrateur: {event}")
        # Invoquer pour obtenir la réponse finale pour vérification
        final_response = orchestrator_app.invoke(inputs)
        print(f"  Réponse finale de l'orchestrateur: {final_response.get('final_response')}")
