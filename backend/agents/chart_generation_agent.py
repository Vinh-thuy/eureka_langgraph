import os
from typing import TypedDict, Literal, List, Union
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Définir l'état spécifique à l'agent de génération de graphiques
class ChartGenerationAgentState(TypedDict):
    question: str
    chart_data: Union[dict, None] # Pour stocker les données du graphique (ex: JSON Plotly)
    chart_type: Union[str, None] # Type de graphique demandé (ex: 'bar', 'line', 'scatter')
    data_source: Union[str, None] # Source des données si spécifiée
    final_response: Union[str, dict] # Message final ou graphique
    conversation_context: dict # Contexte de conversation

# Initialiser le LLM (peut être passé en paramètre ou réutilisé depuis l'orchestrateur)
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

# Fonction pour générer le graphique
def generate_chart(state: ChartGenerationAgentState):
    print("---AGENT GENERATION GRAPHIQUE: GENERATION DU GRAPHIQUE---")
    question = state.get("question", "")
    context = state.get("conversation_context", {})

    # Ici, la logique pour analyser la question, récupérer les données et générer le graphique.
    # Pour l'instant, c'est une maquette.
    # En fonction de la question, on pourrait:
    # 1. Utiliser un outil (tool) pour interroger une base de données ou un fichier.
    # 2. Utiliser le LLM pour structurer la demande de données ou le type de graphique.
    # 3. Exécuter du code Python pour générer le graphique avec Plotly.

    # Exemple simple: simuler la génération d'un graphique Plotly
    import plotly.express as px
    import pandas as pd

    data = {'Category': ['A', 'B', 'C', 'D'], 'Value': [10, 20, 15, 25]}
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Category', y='Value', title='Exemple de graphique généré')

    # Convertir le graphique en JSON pour le passer à Streamlit
    chart_json = fig.to_json()
    print(f"[CHART AGENT] Taille du JSON du graphique généré: {len(chart_json)} caractères")

    return {
        "question": question, # Passer la question pour maintenir l'état
        "chart_data": chart_json,
        "chart_type": "bar",
        "data_source": None, # Pas de source de données dynamique pour l'instant
        "final_response": "Voici le graphique que j'ai généré pour vous.",
        "conversation_context": context
    }

# Fonction pour créer le graphe de l'agent de génération de graphiques
def create_chart_generation_graph():
    workflow = StateGraph(ChartGenerationAgentState)

    workflow.add_node("generate_chart", generate_chart)

    workflow.set_entry_point("generate_chart")
    workflow.add_edge("generate_chart", END)

    return workflow.compile()
