from typing import TypedDict, List
import json
from pathlib import Path
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Définir l'état de l'agent d'analyse d'incident
class IncidentAnalysisAgentState(TypedDict):
    question: str
    response: str
    final_response: str  # Synthèse utilisateur ou réponse finale
    conversation_context: dict  # Pour maintenir le contexte de conversation
    history: List[dict]  # Historique de la conversation
    end_conversation: bool  # Indique si la conversation est terminée
    intermediate_responses: List[dict]  # Pour stocker les réponses intermédiaires
    llm_context: dict  # Contexte enrichi pour le prompt système (clé)
    system_prompt: str  # Prompt système complet pour le LLM


# 2. Définir les fonctions utilitaires
def load_json_data(filename: str) -> dict:
    """Charge les données JSON depuis un fichier"""
    try:
        path = Path(__file__).parent.parent / 'data' / filename
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement de {filename}: {e}")
        return {}


# 3. Définir les nœuds du workflow
def map_incident_to_apps(state: IncidentAnalysisAgentState) -> dict:
    """Étape 1: Mapper l'ID de l'incident aux codes d'application et enrichir le contexte partagé."""
    print("--- ÉTAPE 1: MAPPAGE INCIDENT -> APPLICATIONS ---")
    # Initialisation du contexte partagé
    state.setdefault("llm_context", {})
    # Extraction de l'incident
    incident_id = state.get("conversation_context", {}).get("incident_id")
    if not incident_id:
        incident_digits = "".join(filter(str.isdigit, state['question']))
        incident_id = f"INC{incident_digits}" if incident_digits else "UNKNOWN"
    state["llm_context"]["incident_id"] = incident_id
    # Mapping incident -> applications
    incident_apps_mapping = load_json_data("incident_apps_mapping.json")
    app_codes = incident_apps_mapping.get(incident_id, [])
    state["llm_context"]["applications"] = [{"code": code} for code in app_codes]
    return state


def fetch_application_info(state: IncidentAnalysisAgentState) -> dict:
    """Étape 2 : Récupérer les informations des applications et enrichir le contexte partagé."""
    print("--- ÉTAPE 2: RÉCUPÉRATION DES INFORMATIONS APPLICATIVES ---")
    app_dicts = state["llm_context"].get("applications", [])
    if not app_dicts:
        return state
    apps_data = load_json_data("applications_data.json")
    enriched_apps = []
    for app in app_dicts:
        code = app.get("code")
        info = apps_data.get(code, {})
        enriched_app = {"code": code}
        enriched_app.update(info)
        enriched_apps.append(enriched_app)
    state["llm_context"]["applications"] = enriched_apps
    return state


def display_application_info(state: IncidentAnalysisAgentState) -> dict:
    """Étape 3: Afficher les informations de l'application (réponse immédiate)"""
    print("--- ÉTAPE 3: AFFICHAGE DES INFORMATIONS APPLICATIVES ---")
    
    app_info = state.get("app_info", {})
    incident_id = state.get("conversation_context", {}).get("incident_id", "INCONNU")
    
    # Vérifier si la demande concerne les détails d'une application spécifique
    question = state.get("question", "").lower()
    if "détails" in question and "application" in question:
        # Extraire le code d'application de la question si présent
        app_code = None
        for word in question.split():
            if word.upper().startswith("APP") and len(word) >= 4:  # Ex: APP001
                app_code = word.upper()
                break
        
        if app_code and app_code in app_info:
            # Afficher les détails de l'application spécifique
            info = app_info[app_code]
            response = {
                "type": "intermediate_response",
                "content": f"🔍 Détails de l'application {info.get('name', 'Inconnue')} (Code: {app_code})\n\n"
                          f"- **Propriétaire**: {info.get('owner', 'Non spécifié')}\n"
                          f"- **Environnement**: {info.get('environment', 'Non spécifié')}\n"
                          f"- **Version**: {info.get('version', 'Inconnue')}\n"
                          f"- **Statut**: {info.get('status', 'Inconnu')}\n"
                          f"- **Description**: {info.get('description', 'Aucune description disponible')}",
                "is_final": False
            }
            state["intermediate_responses"] = state.get("intermediate_responses", []) + [response]
            return state
    
    if not app_info:
        response = {
            "type": "intermediate_response",
            "content": f"ℹ️ Aucune information d'application trouvée pour l'incident {incident_id}.",
            "is_final": False
        }
    else:
        # Créer un message utilisateur convivial
        app_list = "\n".join([f"- {info.get('name', 'Sans nom')} (Code: {code})" 
                              for code, info in app_info.items()])
        
        response = {
            "type": "intermediate_response",
            "content": f"🔍 Incident {incident_id} - Applications concernées :\n{app_list}",
            "details": {
                "nombre_applications": len(app_info),
                "codes_applications": list(app_info.keys())
            },
            "is_final": False
        }
    
    # Ajouter la réponse intermédiaire
    state["intermediate_responses"] = state.get("intermediate_responses", []) + [response]
    
    return state

def find_related_incidents(state: IncidentAnalysisAgentState) -> dict:
    """Étape 3: Trouver les incidents corrélés et enrichir le contexte partagé."""
    print("--- ÉTAPE 3: RECHERCHE D'INCIDENTS CORRÉLÉS ---")
    incident_id = state["llm_context"].get("incident_id")
    if not incident_id:
        state["llm_context"]["related_incidents"] = []
        return state
    related_incidents_data = load_json_data("related_incidents.json")
    related_incidents = related_incidents_data.get(incident_id, [])
    state["llm_context"]["related_incidents"] = related_incidents
    return state


def generate_system_prompt(llm_context: dict) -> str:
    """Génère un prompt système structuré à partir du contexte enrichi."""
    prompt = f"""
Vous êtes un expert IT. Voici le contexte complet de l'incident :

Incident ID : {llm_context.get('incident_id', 'N/A')}

Applications concernées :
"""
    for app in llm_context.get('applications', []):
        prompt += f"- {app.get('code', '?')} : {app.get('name', '?')} (Propriétaire : {app.get('owner', '?')})\n"
    prompt += "\nIncidents corrélés :\n"
    for inc in llm_context.get('related_incidents', []):
        prompt += f"- {inc.get('id', '?')} ({inc.get('status', '?')}) : {inc.get('description', '')}\n"
    prompt += "\nRépondez à toute question de l’utilisateur en vous basant uniquement sur ce contexte."
    return prompt


def final_llm_node(state: IncidentAnalysisAgentState) -> dict:
    """
    Dernier nœud : génère :
    1. Un prompt système complet pour le LLM avec tout le contexte
    2. Une synthèse utilisateur courte pour confirmer la disponibilité des données
    """
    print("--- ÉTAPE FINALE : GÉNÉRATION DU PROMPT SYSTÈME ---")
    llm_context = state.get("llm_context", {})
    
    # 1. Générer le prompt complet pour le LLM
    system_prompt = generate_system_prompt(llm_context)
    state["system_prompt"] = system_prompt
    
    # 2. Créer une synthèse utilisateur courte
    incident_id = llm_context.get('incident_id', 'INCONNU')
    app_count = len(llm_context.get('applications', []))
    related_count = len(llm_context.get('related_incidents', []))
    
    summary = (
        f"✅ Analyse prête pour l'incident {incident_id}. "
        f"{app_count} application(s) concernée(s), {related_count} incident(s) corrélé(s).\n\n"
        "Je peux maintenant répondre à vos questions sur cet incident.\n"
        "Exemples :\n"
        "- Quelle est l'application la plus critique ?\n"
        "- Affiche-moi les détails de l'application APP001\n"
        "- Quels sont les incidents corrélés ?"
    )
    
    # Définir la réponse finale avec la synthèse
    state["final_response"] = summary
    
    return state


# 4. Définir le graphe de l'agent d'analyse d'incident
def create_incident_analysis_graph():
    # Créer le graphe de workflow
    workflow = StateGraph(IncidentAnalysisAgentState)
    
    # Ajouter les nœuds au graphe
    workflow.add_node("map_incident_to_apps", map_incident_to_apps)
    workflow.add_node("fetch_app_info", fetch_application_info)
    workflow.add_node("find_related_incidents", find_related_incidents)
    workflow.add_node("final_llm_node", final_llm_node)
    
    # Définir le flux de travail
    workflow.add_edge(START, "map_incident_to_apps")
    workflow.add_edge("map_incident_to_apps", "fetch_app_info")
    workflow.add_edge("fetch_app_info", "find_related_incidents")
    workflow.add_edge("find_related_incidents", "final_llm_node")
    workflow.add_edge("final_llm_node", END)
    
    # Compiler le workflow
    app = workflow.compile()
    
    # Fonction pour initialiser l'état si nécessaire
    def _init_state(state):
        if not state.get("conversation_context"):
            state["conversation_context"] = {}
        if not state.get("history"):
            state["history"] = []
        if "response" not in state:
            state["response"] = ""
        if "final_response" not in state:
            state["final_response"] = ""
        if "end_conversation" not in state:
            state["end_conversation"] = False
        if "intermediate_responses" not in state:
            state["intermediate_responses"] = []
        if "llm_context" not in state:
            state["llm_context"] = {}
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

