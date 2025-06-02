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
    conversation_context: dict  # Pour maintenir le contexte de conversation


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
    
    # Initialiser les champs manquants
    if "question" not in state:
        state["question"] = ""
    
    if "conversation_context" not in state:
        state["conversation_context"] = {}
    
    context = state["conversation_context"]
    question = state["question"]
    
    # Vérifier si on est déjà dans une conversation d'incident
    in_incident_conv = context.get("in_incident_conversation", False)
    
    # Si on est déjà dans une conversation d'incident, on reste sur l'agent d'incident
    if in_incident_conv:
        print("---ORCHESTRATEUR: RESTE DANS LA CONVERSATION D'INCIDENT---")
        print(f"[ROUTEUR] Contexte actuel: {context}")
        state["routing_decision"] = "incident_analysis"
        return state
    
    # Sinon, on route normalement
    try:
        print(f"[ROUTEUR] Question à router: {question}")
        print(f"[ROUTEUR] Contexte actuel: {context}")
        
        # Appeler le routeur seulement si nécessaire
        if not question.strip():
            print("[ROUTEUR] Question vide, utilisation du chatbot générique par défaut")
            state["routing_decision"] = "generic_chatbot"
            return state
            
        # Appeler le routeur pour prendre une décision
        decision = router.invoke([
            SystemMessage(content=router_prompt),
            HumanMessage(content=question),
        ])
        
        print(f"[ROUTEUR] Décision de routage: {decision.step}")
        
        # Mise à jour de l'état avec la décision de routage
        state["routing_decision"] = decision.step
        
        # Si on commence une analyse d'incident, on marque le contexte
        if decision.step == "incident_analysis":
            print("[ROUTEUR] Détection d'une demande d'analyse d'incident")
            context["in_incident_conversation"] = True
            
            # Extraire l'ID d'incident si présent dans la question
            if "INC" in question.upper():
                import re
                match = re.search(r'INC\d+', question.upper())
                if match:
                    context["incident_id"] = match.group(0)
                    print(f"[ROUTEUR] ID d'incident extrait: {context['incident_id']}")
        
        return state
        
    except Exception as e:
        print(f"[ERREUR ROUTEUR] Erreur lors du routage: {str(e)}")
        # Fallback en cas d'échec
        state["routing_decision"] = "generic_chatbot"
        
        # En cas d'erreur, on nettoie le contexte d'incident pour éviter les états bloqués
        if "in_incident_conversation" in context:
            print("[ERREUR ROUTEUR] Nettoyage du contexte d'incident suite à une erreur")
            context.pop("in_incident_conversation", None)
            context.pop("incident_id", None)
    
    return state

def invoke_generic_chatbot_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT GENERIC CHATBOT---")
    
    # --- LOGIQUE DE BOUCLE DE CONVERSATION POUR LE CHATBOT GÉNÉRIQUE ---
    # Cette fonction assure la fluidité multi-tours en conservant l'historique et le contexte conversationnel.
    # Contrairement à l'agent d'incident, il n'y a pas de collecte de données structurées, mais on maintient l'historique pour la cohérence des échanges.
    
    # Initialiser les champs manquants dans l'état
    if "question" not in state:
        state["question"] = ""
    if "conversation_context" not in state:
        state["conversation_context"] = {}
    if "history" not in state:
        state["history"] = []
    
    context = state["conversation_context"]
    question = state["question"]
    history = state["history"]
    
    print(f"[GENERIC CHATBOT] Contexte d'entrée: {context}")
    print(f"[GENERIC CHATBOT] Question: {question}")
    print(f"[GENERIC CHATBOT] Historique: {history[-3:]}")
    
    # --- Gestion de la transition depuis une conversation d'incident ---
    was_in_incident_conv = context.pop("in_incident_conversation", False)
    incident_id = context.pop("incident_id", None)
    if was_in_incident_conv:
        print("---GENERIC CHATBOT: FIN DE LA CONVERSATION D'INCIDENT---")
        if incident_id:
            print(f"[GENERIC CHATBOT] Incident précédent: {incident_id}")
    
    # --- Détection d'intention de sortie (NLU simple) ---
    exit_keywords = ["fin", "stop", "quitter", "merci", "terminé", "au revoir"]
    if any(kw in question.lower() for kw in exit_keywords):
        print("[GENERIC CHATBOT] Fin de conversation détectée (NLU)")
        # Nettoyage du contexte et de l'historique
        context.clear()
        history.clear()
        return {
            "final_response": "Merci pour cette conversation ! N'hésitez pas à revenir si vous avez d'autres questions.",
            "conversation_context": context,
            "history": history
        }

    # --- Ajout de la question courante à l'historique ---
    if question:
        history.append({"role": "user", "content": question})
    
    # --- Génération de la réponse via LLM (prompt simple, contexte = historique) ---
    try:
        # Appel direct au LLM avec l'historique (pas de prompt système spécifique)
        messages = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else SystemMessage(content=msg["content"]) for msg in history]
        llm_response = llm.invoke(messages)
        response = llm_response.content
        print(f"[GENERIC CHATBOT] Réponse générée: {response[:100]}...")
        # Ajout de la réponse à l'historique
        history.append({"role": "assistant", "content": response})
        # Retourner la réponse et le contexte mis à jour
        return {
            "final_response": response,
            "conversation_context": context,
            "history": history
        }
    except Exception as e:
        print(f"[ERREUR GENERIC CHATBOT] Erreur lors de l'appel à l'agent: {str(e)}")
        # En cas d'erreur, on nettoie le contexte pour éviter les états bloqués
        context.pop("in_incident_conversation", None)
        context.pop("incident_id", None)
        return {
            "final_response": "Désolé, une erreur est survenue lors du traitement de votre demande.",
            "conversation_context": context,
            "history": history
        }

# ---
# Cette logique permet de conserver la fluidité et la mémoire de la conversation pour le chatbot générique,
# même sur plusieurs tours, sans workflow structuré ni collecte de données, simplement en stockant l'historique.
# ---

def invoke_incident_analysis_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT INCIDENT ANALYSIS---")
    
    # Initialiser les champs manquants
    if "question" not in state:
        state["question"] = ""
    if "conversation_context" not in state:
        state["conversation_context"] = {}
    if "history" not in state:
        state["history"] = []
    
    context = state["conversation_context"]
    question = state["question"]
    
    print(f"[INCIDENT AGENT] Contexte d'entrée: {context}")
    print(f"[INCIDENT AGENT] Question: {question}")

    # Détection NLU (mots-clés) de l'intention de sortie
    exit_keywords = ["fin", "stop", "quitter", "merci", "terminé", "au revoir"]
    if any(kw in question.lower() for kw in exit_keywords):
        # Mot-clé de sortie détecté, on termine la conversation d'incident
        print("---INCIDENT AGENT: FIN DE LA CONVERSATION D'INCIDENT (mot-clé détecté)---")
        context["in_incident_conversation"] = False
        # Nettoyage de l'historique côté backend
        if "history" in state:
            state["history"].clear()
        return {
            "final_response": "Conversation d’incident terminée. N’hésitez pas à solliciter une nouvelle analyse.",
            "conversation_context": context,
            "history": []
        }
    
    # Vérifier si on a un ID d'incident dans le contexte
    incident_id = context.get("incident_id")
    if not incident_id and "INC" in question.upper():
        # Essayer d'extraire l'ID d'incident de la question
        import re
        match = re.search(r'INC\d+', question.upper())
        if match:
            incident_id = match.group(0)
            context["incident_id"] = incident_id
            print(f"[INCIDENT AGENT] ID d'incident extrait: {incident_id}")
    
    # Vérifier si on est dans une conversation d'incident
    in_incident_conv = context.get("in_incident_conversation", False)
    
    # Si on n'est pas dans une conversation d'incident mais qu'on a un ID, on commence une nouvelle conversation
    if not in_incident_conv and incident_id:
        print(f"[INCIDENT AGENT] Début d'une nouvelle conversation pour l'incident {incident_id}")
        context["in_incident_conversation"] = True
        context["conversation_count"] = 1
    # Si on est déjà dans une conversation, on incrémente le compteur
    elif in_incident_conv:
        context["conversation_count"] = context.get("conversation_count", 0) + 1
        print(f"[INCIDENT AGENT] Suite de la conversation (tour {context['conversation_count']})")
        
        # Appel normal à l'agent d'analyse d'incident (plus de détection NLU ici)
        try:
            # Préparer l'entrée pour l'agent d'analyse d'incident
            incident_analysis_graph = create_incident_analysis_graph()
            incident_analysis_input = {
                "question": question,
                "conversation_context": context.copy(),
                "history": state["history"],
                "current_response": "",
                "end_conversation": False
            }
            print(f"[INCIDENT AGENT] Données envoyées à l'agent: {incident_analysis_input}")
            final_agent_state = incident_analysis_graph.invoke(incident_analysis_input)
            if "conversation_context" in final_agent_state:
                print(f"[INCIDENT AGENT] Contexte retourné: {final_agent_state['conversation_context']}")
                context.update(final_agent_state["conversation_context"])
            else:
                print("[INCIDENT AGENT] Aucun contexte retourné par l'agent")
            # Vérifier si la conversation est terminée
            end_conversation = final_agent_state.get("end_conversation", False)
            if end_conversation:
                print("---INCIDENT AGENT: FIN DE LA CONVERSATION D'INCIDENT---")
                context["in_incident_conversation"] = False
            # Déterminer le nombre de tours de conversation
            conversation_count = context.get("conversation_count", 1)
            system_prompt = final_agent_state.get("system_prompt", "")
            # Récupérer la question utilisateur pour l'appel LLM
            question = state.get("question", "")
            # Par défaut, on renvoie la synthèse courte (premier tour)
            response = final_agent_state.get(
                "final_response",
                final_agent_state.get(
                    "current_response",
                    final_agent_state.get(
                        "response",
                        "Désolé, je n'ai pas pu traiter votre demande d'incident."
                    )
                )
            )
            print(f"[DEBUG] conversation_count={conversation_count}, system_prompt not empty? {bool(system_prompt)}")
            # Si on est dans la boucle conversationnelle (après synthèse), on appelle le LLM avec le contexte enrichi
            if conversation_count > 1 and system_prompt:
                try:
                    from langchain_core.messages import SystemMessage, HumanMessage
                    llm_response = llm.invoke([
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=question)
                    ])
                    response = llm_response.content
                    print(f"[INCIDENT AGENT] Réponse LLM générée: {response[:100]}...")
                except Exception as e:
                    print(f"[INCIDENT AGENT] Erreur lors de l'appel LLM: {e}")
                    response = "Désolé, une erreur est survenue lors de la génération de la réponse contextuelle."
            else:
                print(f"[INCIDENT AGENT] Réponse générée (synthèse): {response[:100]}...")
            # Retourner la réponse et le contexte mis à jour
            return {
                "final_response": response,
                "conversation_context": context
            }
        except Exception as e:
            print(f"[ERREUR INCIDENT AGENT] Erreur lors de l'appel à l'agent: {str(e)}")
            # En cas d'erreur, on nettoie le contexte d'incident pour éviter les états bloqués
            context.pop("in_incident_conversation", None)
            context.pop("incident_id", None)
            return {
                "final_response": "Désolé, une erreur est survenue lors du traitement de votre demande d'incident.",
                "conversation_context": context
            }

def fallback_node(state: OrchestratorState):
    print("---ORCHESTRATEUR: NŒUD PAR DÉFAUT (FALLBACK)---")
    return {"final_response": "Désolé, je ne peux pas traiter ce type de demande pour le moment. Essayez une recherche de recette ou d'appartement."}

# 3. Définir les arêtes conditionnelles
def decide_next_node(state: OrchestratorState):
    print("---ORCHESTRATEUR: DÉCISION DU PROCHAIN NŒUD---")
    
    # Initialiser les champs manquants
    if "routing_decision" not in state:
        state["routing_decision"] = "generic_chatbot"
    if "conversation_context" not in state:
        state["conversation_context"] = {}
    
    context = state["conversation_context"]
    print(f"[DECIDE NEXT NODE] Contexte actuel: {context}")
    print(f"[DECIDE NEXT NODE] Décision de routage: {state['routing_decision']}")
    
    # Si on est dans une conversation d'incident, on reste sur l'agent d'incident
    if context.get("in_incident_conversation", False):
        print("[DECIDE NEXT NODE] Reste dans la conversation d'incident")
        return "incident_analysis_agent"  # Retourne le nom du nœud tel que défini dans create_orchestrator_graph
    
    # Si on a une décision de routage, on la suit
    if state["routing_decision"] == "incident_analysis":
        print("[DECIDE NEXT NODE] Routage vers l'analyse d'incident")
        
        # Extraire l'ID d'incident de la question si possible
        question = state.get("question", "")
        if "INC" in question.upper():
            import re
            match = re.search(r'INC\d+', question.upper())
            if match:
                context["incident_id"] = match.group(0)
                print(f"[DECIDE NEXT NODE] ID d'incident extrait: {context['incident_id']}")
        
        return "incident_analysis_agent"  # Retourne le nom du nœud tel que défini dans create_orchestrator_graph
    
    # Par défaut, on utilise le chatbot générique
    print("[DECIDE NEXT NODE] Utilisation du chatbot générique par défaut")
    return "generic_chatbot_agent"  # Retourne le nom du nœud tel que défini dans create_orchestrator_graph

# 4. Construire le graphe de l'orchestrateur
def create_orchestrator_graph():
    workflow = StateGraph(OrchestratorState)

    # Ajouter les nœuds
    workflow.add_node("router", route_question)
    workflow.add_node("generic_chatbot_agent", invoke_generic_chatbot_agent)
    workflow.add_node("incident_analysis_agent", invoke_incident_analysis_agent)
    workflow.add_node("fallback", fallback_node)

    # Définir le point d'entrée
    workflow.set_entry_point("router")

    # Ajouter les arêtes conditionnelles
    workflow.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "generic_chatbot_agent": "generic_chatbot_agent",
            "incident_analysis_agent": "incident_analysis_agent",
            "fallback": "fallback",
        },
    )

    # Ajouter les arêtes de sortie
    workflow.add_edge("generic_chatbot_agent", END)
    workflow.add_edge("incident_analysis_agent", END)
    workflow.add_edge("fallback", END)
    
    # Compiler le workflow
    app = workflow.compile()
    
    # Fonction pour initialiser l'état si nécessaire
    def _init_state(state):
        if not state.get("conversation_context"):
            state["conversation_context"] = {}
        if not state.get("history"):
            state["history"] = []
        if not state.get("routing_decision"):
            state["routing_decision"] = "generic_chatbot"
        if not state.get("final_response"):
            state["final_response"] = ""
        return state
    
    # Envelopper la fonction invoke pour gérer l'initialisation
    original_invoke = app.invoke
    
    def wrapped_invoke(input_state):
        # Initialiser l'état
        state = _init_state(input_state.copy())
        print(f"[ORCHESTRATEUR] État initialisé: {state.keys()}")
        # Appeler la fonction originale
        result = original_invoke(state)
        print(f"[ORCHESTRATEUR] Résultat après invocation: {result.keys() if isinstance(result, dict) else 'N/A'}")
        return result
    
    app.invoke = wrapped_invoke
    
    return app

