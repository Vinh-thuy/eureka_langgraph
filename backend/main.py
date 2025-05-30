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
    if orchestrator_graph is None:
        return JSONResponse(status_code=503, content={"error": "Service temporairement indisponible: l'orchestrateur n'a pas pu être initialisé."})

    try:
        data = await request.json()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Requête JSON invalide: {str(e)}"})

    question = data.get("question", "")
    history = data.get("history", [])

    if not question:
        return JSONResponse(status_code=400, content={"error": "La question ne peut pas être vide."})

    try:
        orchestrator_input = {"question": question, "history": history}
        
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(None, orchestrator_graph.invoke, orchestrator_input)
        
        response_content = final_state.get("final_response", "Désolé, une réponse attendue n'a pas été trouvée dans l'état final.")
        
        return JSONResponse(content={"answer": response_content})

    except Exception as e:
        # Log l'erreur côté serveur pour le débogage
        print(f"[ERREUR /ask] Exception lors de l'invocation de l'orchestrateur ou du traitement: {type(e).__name__}: {e}")
        # Réponse générique à l'utilisateur pour des raisons de sécurité
        return JSONResponse(status_code=500, content={"error": "Une erreur interne est survenue lors du traitement de votre demande."})
