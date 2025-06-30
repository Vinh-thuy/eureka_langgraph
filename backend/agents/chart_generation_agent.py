import os
from typing import TypedDict, Union
import plotly.express as px
import pandas as pd
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

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

    # Fonction utilitaire pour générer des données de graphique et la figure Plotly
    def _generate_plot_data(chart_type):
        data = {'Category': ['A', 'B', 'C', 'D'], 'Value': [10, 20, 15, 25]}
        df = pd.DataFrame(data)
        fig = None

        if chart_type == 'bar':
            fig = px.bar(df, x='Category', y='Value', title='Exemple de Bar Plot')
        elif chart_type == 'pie':
            fig = px.pie(df, values='Value', names='Category', title='Exemple de Pie Chart')
        # Ajoutez d'autres types de graphiques ici
        
        return fig

    # Simuler l'extraction des types de graphiques de la question
    # Dans une application réelle, cela impliquerait une analyse NLP plus sophistiquée
    def _extract_chart_types_from_question(question_text):
        chart_types = []
        if "bar" in question_text.lower():
            chart_types.append('bar')
        if "pie" in question_text.lower():
            chart_types.append('pie')
        if not chart_types:
            chart_types.append('bar') # Par défaut, générer un bar chart
        return chart_types



    requested_chart_types = _extract_chart_types_from_question(question)
    generated_charts_json = []

    for chart_type in requested_chart_types:
        fig = _generate_plot_data(chart_type)
        if fig:
            chart_json = fig.to_json()
            generated_charts_json.append(chart_json)
            print(f"[CHART AGENT] Taille du JSON du {chart_type} généré: {len(chart_json)} caractères")

    return {
        "question": question, # Passer la question pour maintenir l'état
        "chart_data": generated_charts_json, # Maintenant une liste de JSON de graphiques
        "chart_type": requested_chart_types, # Peut être une liste de types
        "data_source": None, # Pas de source de données dynamique pour l'instant
        "final_response": "Voici les graphiques que j'ai générés pour vous.",
        "conversation_context": context
    }

# Fonction pour créer le graphe de l'agent de génération de graphiques
def create_chart_generation_graph():
    workflow = StateGraph(ChartGenerationAgentState)

    workflow.add_node("generate_chart", generate_chart)

    workflow.set_entry_point("generate_chart")
    workflow.add_edge("generate_chart", END)

    return workflow.compile()
