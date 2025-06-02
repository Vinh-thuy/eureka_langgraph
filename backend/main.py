from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pathlib
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import asyncio
from agents import create_orchestrator_graph

load_dotenv()

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR.parent / "images"
if not IMAGES_DIR.exists():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[DEBUG] Le dossier images a été créé à: {IMAGES_DIR}")

print(f"[DEBUG] Les images seront servies depuis: {IMAGES_DIR}")
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator_graph = None
try:
    orchestrator_graph = create_orchestrator_graph()
    print("[INFO] Orchestrateur LangGraph initialisé avec succès.")
except ImportError as e:
    print(f"[ERREUR FATALE] Erreur d'importation lors de la création de l'orchestrateur: {e}")
    print("[ERREUR FATALE] Assurez-vous que le package 'agents' est correctement structuré et accessible (ex: backend/agents/__init__.py).")
except Exception as e:
    print(f"[ERREUR FATALE] Erreur inattendue lors de la création de l'orchestrateur: {e}")

@app.get("/")
def read_root():
    if orchestrator_graph is None:
        return {"message": "Backend IA démarré, mais ERREUR lors de l'initialisation de l'orchestrateur LangGraph!"}
    return {"message": "Backend IA prêt avec LangGraph Orchestrator!"}

@app.post("/ask")
async def ask_bot(request: Request):
    """
    Endpoint pour poser une question au chatbot.
    Gère le contexte de conversation entre les requêtes.
    """
    print("\n=== NOUVELLE REQUÊTE /ask ===")
    
    # Vérifier que l'orchestrateur est initialisé
    if orchestrator_graph is None:
        error_msg = "Service temporairement indisponible: l'orchestrateur n'a pas pu être initialisé."
        print(f"[ERREUR] {error_msg}")
        return JSONResponse(
            status_code=503, 
            content={"error": error_msg}
        )

    # Parser la requête JSON
    try:
        data = await request.json()
        print(f"[REQUEST] Données reçues: {data.keys()}")
    except Exception as e:
        error_msg = f"Requête JSON invalide: {str(e)}"
        print(f"[ERREUR] {error_msg}")
        return JSONResponse(
            status_code=400, 
            content={"error": error_msg}
        )

    # Extraire les données de la requête avec des valeurs par défaut
    question = data.get("question", "").strip()
    history = data.get("history", [])
    conversation_context = data.get("conversation_context", {})
    
    print(f"[TRAITEMENT] Question: {question[:100]}...")
    print(f"[TRAITEMENT] Taille de l'historique: {len(history)}")
    print(f"[TRAITEMENT] Contexte reçu: {conversation_context}")

    # Valider la question
    if not question:
        error_msg = "La question ne peut pas être vide."
        print(f"[ERREUR] {error_msg}")
        return JSONResponse(
            status_code=400, 
            content={"error": error_msg}
        )

    try:
        # Préparer l'entrée pour l'orchestrateur
        orchestrator_input = {
            "question": question,
            "history": history,
            "conversation_context": conversation_context,
            "final_response": "",
            "routing_decision": ""
        }
        
        print("[TRAITEMENT] Appel de l'orchestrateur...")
        
        # Exécuter le graphe d'orchestration de manière asynchrone
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, 
            lambda: orchestrator_graph.invoke(orchestrator_input)
        )
        
        # Extraire la réponse et le contexte mis à jour
        response_content = final_state.get(
            "final_response", 
            "Désolé, je n'ai pas pu générer de réponse."
        )
        
        updated_context = final_state.get("conversation_context", {})
        
        print(f"[RÉPONSE] Taille de la réponse: {len(str(response_content))} caractères")
        print(f"[RÉPONSE] Contexte mis à jour: {updated_context}")
        
        # Retourner la réponse au format standard
        return JSONResponse(content={
            "answer": response_content,
            "conversation_context": updated_context
        })

    except Exception as e:
        # Log l'erreur complète pour le débogage
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERREUR CRITIQUE] {str(e)}\n{error_details}")
        
        # En cas d'erreur, on nettoie le contexte pour éviter les états incohérents
        if isinstance(conversation_context, dict):
            conversation_context.pop("in_incident_conversation", None)
            conversation_context.pop("incident_id", None)
        
        # Réponse d'erreur détaillée en mode debug, générique en production
        error_response = {
            "error": "Une erreur est survenue lors du traitement de votre demande.",
            "details": str(e) if app.debug else None,
            "conversation_context": conversation_context
        }
        
        return JSONResponse(
            status_code=500, 
            content=error_response
        )
