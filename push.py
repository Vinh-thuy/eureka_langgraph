def invoke_incident_analysis_agent(state: OrchestratorState):
    print("---ORCHESTRATEUR: INVOCATION DE L'AGENT INCIDENT ANALYSIS---")
    
    # Initialisation des champs
    state.setdefault("question", "")
    state.setdefault("conversation_context", {})
    state.setdefault("history", [])
    
    context = state["conversation_context"]
    question = state["question"]
    
    print(f"[INCIDENT AGENT] Contexte d'entrée: {context}")
    print(f"[INCIDENT AGENT] Question: {question}")

    # Détection des mots-clés de sortie
    exit_keywords = ["fin", "stop", "quitter", "merci", "terminé", "au revoir"]
    if any(kw in question.lower() for kw in exit_keywords):
        print("---INCIDENT AGENT: FIN DE LA CONVERSATION D'INCIDENT (mot-clé détecté)---")
        context["in_incident_conversation"] = False
        state["history"].clear()
        return {
            "final_response": "Conversation d'incident terminée. N'hésitez pas à solliciter une nouvelle analyse.",
            "conversation_context": context,
            "history": []
        }
    
    # Extraction de l'ID d'incident si présent dans la question
    incident_id = context.get("incident_id")
    if not incident_id and "INC" in question.upper():
        import re
        match = re.search(r'INC\d+', question.upper())
        if match:
            incident_id = match.group(0)
            context["incident_id"] = incident_id
            print(f"[INCIDENT AGENT] ID d'incident extrait: {incident_id}")
    
    # Vérification de l'état de la conversation
    in_incident_conv = context.get("in_incident_conversation", False)
    
    # Vérification pour l'utilisation directe du LLM
    if in_incident_conv and context.get("conversation_count", 0) > 0 and "system_prompt" in context:
        print("[INCIDENT AGENT] Utilisation directe du LLM avec le contexte existant")
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            llm_response = llm.invoke([
                SystemMessage(content=context["system_prompt"]),
                HumanMessage(content=question)
            ])
            return {
                "final_response": llm_response.content,
                "conversation_context": context,
                "meta": {
                    "use_case": "incident_analysis",
                    "subgraph": "Analyse d'incident",
                    "incident_id": context.get("incident_id")
                }
            }
        except Exception as e:
            print(f"[INCIDENT AGENT] Erreur avec l'appel direct: {e}")
            # On continue avec le traitement normal en cas d'erreur
    
    # Gestion du compteur de conversation
    if not in_incident_conv and incident_id:
        # Nouvelle conversation
        print(f"[INCIDENT AGENT] Début d'une nouvelle conversation pour l'incident {incident_id}")
        context["in_incident_conversation"] = True
        context["conversation_count"] = 1
    elif in_incident_conv:
        # Suite de conversation
        context["conversation_count"] = context.get("conversation_count", 0) + 1
        print(f"[INCIDENT AGENT] Suite de la conversation (tour {context['conversation_count']})")
    
    # Exécution du graphe d'analyse
    try:
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
        
        # Mise à jour du contexte
        if "conversation_context" in final_agent_state:
            context.update(final_agent_state["conversation_context"])
        
        # Gestion de la fin de conversation
        end_conversation = final_agent_state.get("end_conversation", False)
        if end_conversation:
            print("---INCIDENT AGENT: FIN DE LA CONVERSATION D'INCIDENT---")
            context["in_incident_conversation"] = False
        
        # Récupération de la réponse
        response = final_agent_state.get(
            "current_response",
            final_agent_state.get(
                "response",
                "Désolé, je n'ai pas pu traiter votre demande d'incident."
            )
        )
        
        return {
            "final_response": response,
            "conversation_context": context,
            "meta": {
                "use_case": "incident_analysis",
                "subgraph": "Analyse d'incident",
                "incident_id": context.get("incident_id")
            }
        }
        
    except Exception as e:
        print(f"[ERREUR INCIDENT AGENT] Erreur lors de l'appel à l'agent: {str(e)}")
        context.update({
            "in_incident_conversation": False,
            "incident_id": None
        })
        return {
            "final_response": "Désolé, une erreur est survenue lors du traitement de votre demande d'incident.",
            "conversation_context": context
        }
