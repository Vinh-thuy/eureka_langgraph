from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# 1. Définir l'état de l'agent d'appartements
class ApartmentAgentState(TypedDict):
    question: str
    apartment_listing: str

# 2. Définir les nœuds de l'agent
def find_apartment(state: ApartmentAgentState):
    print("---AGENT APPARTEMENTS: RECHERCHE D'APPARTEMENT---")
    question = state['question']
    # Simuler la recherche d'un appartement
    listing = f"Voici une annonce pour '{question}': Bel appartement T3, lumineux, proche commerces. Loyer: 1200€."
    return {"apartment_listing": listing}

# 3. Définir le graphe de l'agent d'appartements
def create_apartment_graph():
    workflow = StateGraph(ApartmentAgentState)
    workflow.add_node("find_apartment", find_apartment)
    workflow.add_edge(START, "find_apartment")
    workflow.add_edge("find_apartment", END)
    app = workflow.compile()
    return app

if __name__ == "__main__":
    apartment_app = create_apartment_graph()
    inputs = {"question": "appartement à louer à Paris"}
    print("\nTest de l'agent d'appartements:")
    for event in apartment_app.stream(inputs):
        for k, v in event.items():
            print(f"  Événement: {k}: {v}")
    final_state = apartment_app.invoke(inputs)
    print(f"  Réponse finale: {final_state.get('apartment_listing')}")
