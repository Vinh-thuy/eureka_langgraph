# Chatbot d'Analyse d'Incidents IT

Ce projet propose un système avancé de gestion et d'analyse d'incidents IT, utilisant des techniques d'IA pour faciliter le diagnostic et la résolution des problèmes techniques. L'application permet de maintenir le contexte des conversations et de gérer des flux de travail complexes pour l'analyse d'incidents.

## Fonctionnalités Principales

- **Gestion de contexte de conversation** : Maintien de l'état de la conversation entre les requêtes
- **Analyse d'incidents** : Détection et suivi des numéros d'incident (format INC suivi de chiffres)
- **Routage intelligent** : Distribution des requêtes entre différents agents spécialisés
- **Interface utilisateur intuitive** : Affichage clair des messages et des images associées

## Architecture de la Boucle de Conversation

### Conversation Générique (Chatbot)

Pour le chatbot générique, la logique de gestion de la conversation est similaire à celle de l'incident, mais sans collecte de données structurées :

- **Objectif** : Permettre des échanges fluides et cohérents sur plusieurs tours, même autour d'une thématique, sans repartir de zéro à chaque question.
- **Historique** : À chaque question, l'historique complet de la conversation (questions/réponses) est transmis au LLM, permettant au chatbot de garder le fil de la discussion.
- **Pas de contexte structuré** : Contrairement à l'analyse d'incident, il n'y a pas de sous-graphe de collecte ou de prompt système enrichi, seulement l'historique qui sert de mémoire.
- **Sortie** : L'utilisateur peut quitter la conversation à tout moment, l'historique est alors réinitialisé ou conservé selon le besoin.

Exemple de scénario :

1. Utilisateur : "Explique-moi la blockchain."
2. Chatbot : [réponse détaillée]
3. Utilisateur : "Et ses applications concrètes ?"
4. Chatbot : [réponse contextuelle, car il se souvient du sujet précédent]

---

Le système utilise une architecture modulaire avec une séparation claire entre la collecte d'informations et la gestion de la conversation :

### 1. Sous-graphe d'Analyse d'Incident
- **Rôle** : Collecte et structure les données liées à un incident
- **Actions** :
  - Récupère les informations sur l'incident (applications impactées, incidents liés, etc.)
  - Génère un `system_prompt` complet avec toutes les données structurées
  - Produit une synthèse initiale pour l'utilisateur
- **Exécution** : Ne s'exécute qu'une seule fois au début de la conversation

### 2. Orchestrateur Principal
- **Rôle** : Gère la conversation sur plusieurs tours
- **Fonctionnalités** :
  - Maintient l'état de la conversation (`in_incident_conversation`, compteur de tours)
  - Appelle le LLM pour chaque nouvelle question en utilisant le `system_prompt` initial
  - Gère l'historique des messages
  - Détecte les intentions de sortie (ex: "fin", "merci")

### 3. Flux de Données
```
[Utilisateur] 
     |→ [Orchestrateur] → [Sous-graphe] (premier tour uniquement)
          |→ [LLM avec system_prompt + historique] (tours suivants)
               |→ [Réponse à l'utilisateur]
```

## Structure du Projet

- `frontend/` : Interface utilisateur réactive (React)
- `backend/` : API et logique métier (FastAPI + LangGraph)
  - `agents/` : Différents agents spécialisés
    - `incident_analysis_agent.py` : Gère l'analyse des incidents IT
    - `generic_chatbot_agent.py` : Gère les conversations générales
    - `orchestrator.py` : Orchestre le routage entre les agents
- `images/` : Ressources visuelles pour l'application

## Prérequis

- Python 3.8+ (ne pas utiliser 3.13)
- Node.js 16+
- npm ou yarn

## Installation

### 1. Configuration du backend

```bash
# Se placer dans le répertoire du projet (remplacez par votre chemin si nécessaire)
cd ~/Documents/eureka_langgraph

# Créer un environnement virtuel
python3 -m venv venv  # Utilisez python3 sur Mac/Linux

# Activer l'environnement virtuel
# Sur Mac/Linux :
source venv/bin/activate
# Sur Windows :
# .\venv\Scripts\activate

# Installer les dépendances Python
pip install -r backend/requirements.txt
```

### 2. Configuration du frontend

```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances Node.js
npm install
```

## Lancement de l'application

### 1. Démarrer le serveur backend

Dans un terminal :

```bash
# Activer l'environnement virtuel si ce n'est pas déjà fait
source venv/bin/activate  # Sur Mac/Linux
# ou venv\Scripts\activate sur Windows

# Se placer dans le dossier backend
cd backend

# Lancer le serveur FastAPI
uvicorn main:app --reload
```

### 2. Démarrer le serveur frontend

Dans un autre terminal :

```bash
# Se placer dans le dossier frontend
cd frontend

# Démarrer le serveur de développement
npm run dev
```

## Accès à l'application

- **Interface utilisateur** : Ouvrez votre navigateur à l'adresse indiquée par Vite (généralement `http://localhost:5173`)
- **API Backend** : L'API sera disponible sur `http://localhost:8000`
- **Documentation de l'API** : `http://localhost:8000/docs` (Swagger UI)

## Gestion du Contexte de Conversation

Le système maintient un contexte de conversation qui permet de :
- Suivre l'état actuel de la conversation
- Conserver les informations sur l'incident en cours d'analyse
- Maintenir un compteur de tours de conversation

### Comment utiliser l'analyse d'incidents

1. **Démarrer une analyse** : 
   ```
   Analyse l'incident INC12345
   ```
2. **Poser des questions de suivi** :
   ```
   Quels sont les changements suspects ?
   ```
3. **Terminer la conversation** :
   ```
   Fin de la conversation
   ```

## Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet avec les variables nécessaires :

```env
# Clé API OpenAI (obligatoire)
OPENAI_API_KEY=votre_cle_api_openai

# Configuration du backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Configuration du frontend
VITE_API_URL=http://localhost:8000

# Niveau de logs (optionnel)
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Développement

### Améliorations Récentes

- **v1.0** : Implémentation de la gestion du contexte de conversation
  - Maintien de l'état entre les requêtes
  - Support des conversations multi-tours
  - Gestion des numéros d'incident

### Personnalisation

- **Agents** : Ajoutez de nouveaux agents dans le dossier `backend/agents/`
- **Styles** : Personnalisez l'interface dans `frontend/src/`
- **Prompts** : Modifiez les prompts dans les fichiers des agents
- **Logs** : Niveaux de logs configurables pour le débogage

### Tests

Pour tester le bon fonctionnement :
1. Démarrer le backend et le frontend
2. Essayer une conversation d'incident complète
3. Vérifier la conservation du contexte
4. Tester différentes requêtes de suivi

