from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pathlib
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import asyncio
from agents import create_orchestrator_graph
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Dict, Any, Optional
from pydantic import BaseModel

load_dotenv()

# ===== DÉBUT GESTION DES SESSIONS FASTAPI =====
# Stockage en mémoire des sessions (à remplacer par Redis en production pour un usage réel)
# Note: En production, utilisez un stockage persistant comme Redis
sessions: Dict[str, Dict[str, Any]] = {}

def cleanup_inactive_sessions():
    """
    Nettoie les sessions inactives depuis plus d'une heure.
    Cette fonction est appelée périodiquement par le middleware de session.
    """
    now = datetime.now()
    inactive_sessions = [
        session_id for session_id, session_data in sessions.items()
        if now - session_data.get("last_activity", now) > timedelta(hours=1)
    ]
    for session_id in inactive_sessions:
        del sessions[session_id]
# ===== FIN GESTION DES SESSIONS FASTAPI =====


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

# ===== DÉBUT MIDDLEWARE DE SESSION FASTAPI =====
# Ce middleware gère automatiquement les sessions utilisateur
# Il est exécuté avant chaque requête HTTP
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # ===== DÉBUT MODIF: GESTION AMÉLIORÉE DES SESSIONS =====
    try:
        # 1. Récupérer ou créer un ID de session
        session_id = request.cookies.get("session_id")
        
        if not session_id or session_id not in sessions:
            session_id = str(uuid4())
            sessions[session_id] = {
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "context": {},
                "history": [],
                "routing_decision": ""
            }
        
        # 2. Récupérer les données de session
        session_data = sessions[session_id]
        
        # 3. Mettre à jour le timestamp d'activité
        session_data["last_activity"] = datetime.now()
        
        # 4. Nettoyage périodique (toutes les 10 requêtes)
        if len(sessions) % 10 == 0:
            cleanup_inactive_sessions()
        
        # 5. Ajouter la session à la requête
        request.state.session = session_data
        request.state.session_id = session_id
        
        # 6. Traiter la requête
        response = await call_next(request)
        
        # 7. Mettre à jour le cookie de session dans la réponse
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=3600 * 24 * 7,  # 1 semaine
            samesite="lax",
            secure=False,  # Mettre à True en production avec HTTPS
            path="/"
        )
        
        # 8. Sauvegarder les modifications de la session
        sessions[session_id] = session_data
        return response
        
    except Exception as e:
        print(f"[ERREUR SESSION] {str(e)}")
        raise
    # ===== FIN MODIF =====
# ===== FIN MIDDLEWARE DE SESSION FASTAPI =====
# ===== FIN MIDDLEWARE DE SESSION FASTAPI =====


orchestrator_graph = None
try:
    orchestrator_graph = create_orchestrator_graph()
    print("[INFO] Orchestrateur LangGraph initialisé avec succès.")
except ImportError as e:
    print(f"[ERREUR FATALE] Erreur d'importation lors de la création de l'orchestrateur: {e}")
    print("[ERREUR FATALE] Assurez-vous que le package 'agents' est correctement structuré et accessible (ex: backend/agents/__init__.py).")
except Exception as e:
    print(f"[ERREUR FATALE] Erreur inattendue lors de la création de l'orchestrateur: {e}")


class ChatRequest(BaseModel):
    """Modèle pour la requête de chat"""
    question: str
    context: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Bonjour, comment puis-je vous aider ?",
                "context": {}
            }
        }


@app.get("/")
def read_root():
    if orchestrator_graph is None:
        return {"message": "Backend IA démarré, mais ERREUR lors de l'initialisation de l'orchestrateur LangGraph!"}
    return {"message": "Backend IA prêt avec LangGraph Orchestrator!"}


@app.post("/ask")
async def ask_bot(chat_request: ChatRequest, request: Request):
    """
    Endpoint pour poser une question au chatbot.
    
    Args:
        chat_request (ChatRequest): La requête contenant la question et le contexte optionnel
        request: La requête HTTP (gérée automatiquement par FastAPI)
        
    Returns:
        dict: La réponse du chatbot avec la clé 'final_response' et des métadonnées
    """
    # ===== GESTION DE SESSION DANS /ask =====
    # Récupération de la session utilisateur depuis le middleware
    # La session contient l'historique et le contexte de conversation
    session = request.state.session
    session_id = request.state.session_id
    
    print(f"\n=== NOUVELLE REQUÊTE /ask - Session: {session_id} ===")
    
    # Vérifier que l'orchestrateur est initialisé
    if orchestrator_graph is None:
        error_msg = "Service temporairement indisponible: l'orchestrateur n'a pas pu être initialisé."
        print(f"[ERREUR] {error_msg}")
        return JSONResponse(
            status_code=503, 
            content={"error": error_msg}
        )

    # Utilisation directe du modèle Pydantic
    question = chat_request.question.strip()
    if chat_request.context:
        request.state.session["context"].update(chat_request.context)
    
    # Récupération des données de session
    # Ces données persistent entre les requêtes pour le même utilisateur
    history = session.get("history", [])
    conversation_context = session.get("context", {})
    
    print(f"[SESSION] ID: {session_id}")
    print(f"[TRAITEMENT] Question: {question[:100]}...")
    print(f"[TRAITEMENT] Taille de l'historique: {len(history)}")
    print(f"[TRAITEMENT] Contexte de session: {conversation_context}")

    # Validation de la question (gérée par Pydantic, mais on garde une vérification)
    if not question:
        raise HTTPException(
            status_code=400,
            detail={"error": "La question ne peut pas être vide"}
        )

    try:
        # ===== DÉBUT MODIF: PRÉPARATION ENTRÉE ORCHESTRATEUR =====
        # Modifier cette section pour inclure tous les champs nécessaires
        orchestrator_input = {
            "question": question,
            "history": history,
            "conversation_context": conversation_context,
            "final_response": "",
            "routing_decision": session.get("routing_decision", ""),  # Conserver la décision de routage
            "meta": {}  # Champ nécessaire pour éviter les erreurs
        }
        # ===== FIN MODIF =====
        
        print("[TRAITEMENT] Appel de l'orchestrateur...")
        
        # Exécuter le graphe d'orchestration de manière asynchrone
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, 
            lambda: orchestrator_graph.invoke(orchestrator_input)
        )
        
        # ===== DÉBUT MODIF: MISE À JOUR SESSION =====
        # Mise à jour de la session avec les nouvelles données
        if "history" in final_state:
            session["history"] = final_state["history"]
        if "conversation_context" in final_state:
            session["context"] = final_state["conversation_context"]
        if "routing_decision" in final_state:
            session["routing_decision"] = final_state["routing_decision"]
            
        # Pour le débogage
        session["last_question"] = question
        session["last_response"] = final_state.get("final_response", "")
        # ===== FIN MODIF =====
        
        # Préparer la réponse
        response_content = final_state.get(
            "final_response", 
            "Désolé, je n'ai pas pu générer de réponse."
        )
        
        print(f"[RÉPONSE] Taille de la réponse: {len(str(response_content))} caractères")
        print(f"[SESSION] Historique mis à jour pour la session {session_id}")
        
        # Retourner la réponse au format standard
        return {
            "final_response": response_content,
            "meta": final_state.get("meta", {}),
            "generated_chart": final_state.get("generated_chart", []) # S'attendre à une liste de graphiques
        }

    except Exception as e:
        # Log l'erreur complète pour le débogage
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERREUR CRITIQUE] {str(e)}\n{error_details}")
        
        # En cas d'erreur, on nettoie le contexte de la session
        # pour éviter des états incohérents
        if isinstance(conversation_context, dict):
            conversation_context.pop("in_incident_conversation", None)
            conversation_context.pop("incident_id", None)
            session["context"] = conversation_context  # Sauvegarde en session
        # ===== FIN GESTION D'ERREUR =====
        # La session est automatiquement sauvegardée grâce au middleware
        
        # Réponse d'erreur
        return JSONResponse(
            status_code=500,
            content={
                "error": "Une erreur est survenue lors du traitement de votre demande.",
                "details": str(e) if app.debug else None
            }
        )
