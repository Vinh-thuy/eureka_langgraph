from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Définir l'état de l'agent de recettes
class RecipeAgentState(TypedDict):
    question: str
    recipe_details: str

# 2. Définir les nœuds de l'agent
def find_recipe(state: RecipeAgentState):
    print("---AGENT RECETTES: RECHERCHE DE RECETTE---")
    question = state['question']
    # Simuler la recherche d'une recette
    recipe = f"Voici une recette simple pour '{question}': Mélangez des ingrédients et faites cuire. Bon appétit !"
    return {"recipe_details": recipe}

# 3. Définir le graphe de l'agent de recettes
def create_recipe_graph():
    workflow = StateGraph(RecipeAgentState)
    workflow.add_node("find_recipe", find_recipe)
    workflow.add_edge(START, "find_recipe")
    workflow.add_edge("find_recipe", END)
    app = workflow.compile()
    return app

if __name__ == "__main__":
    recipe_app = create_recipe_graph()
    inputs = {"question": "comment faire un gateau au chocolat"}
    print("\nTest de l'agent de recettes:")
    for event in recipe_app.stream(inputs):
        for k, v in event.items():
            print(f"  Événement: {k}: {v}")
    final_state = recipe_app.invoke(inputs)
    print(f"  Réponse finale: {final_state.get('recipe_details')}")
