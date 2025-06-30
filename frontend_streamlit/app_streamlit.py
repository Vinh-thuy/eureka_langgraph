import streamlit as st
import requests
import plotly.express as px
import pandas as pd

import plotly.io as pio # Import pour la gestion des objets Plotly


st.set_page_config(page_title="Stream Digital Twin", page_icon="📊", layout="wide")

# --- CSS custom pour une UI moderne ---
st.markdown('''
<style>
/* Styles pour le conteneur principal */
.main-container {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 2rem);
    gap: 1rem;
    padding: 1rem;
}

/* Colonne de gauche pour les graphiques */
.graph-column {
    flex: 1;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 8px #00000010;
    overflow-y: auto;
    max-height: calc(100vh - 4rem);
}

/* Colonne de droite pour le chat */
.chat-column {
    width: 40%;
    min-width: 400px;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 4rem);
}

/* Styles pour la zone de chat */
.chat-container {
    flex-grow: 1;
    overflow-y: auto;
    padding: 1rem;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px #00000010;
    margin-bottom: 1rem;
}

/* Styles des bulles de chat */
.bubble-user {
    background: #1976D2;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    text-align: right;
    box-shadow: 0 2px 8px #1976d220;
}

.bubble-bot {
    background: #f5f5f5;
    color: #222;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    margin: 8px auto 8px 0;
    max-width: 75%;
    text-align: left;
    box-shadow: 0 2px 8px #8882;
    position: relative;
}

/* Zone de saisie */
.input-container {
    background: #fff;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 -2px 8px #00000005;
}

/* Badges et éléments divers */
.badge-incident {
    display: inline-block;
    background: #1976D2;
    color: #fff;
    font-weight: bold;
    border-radius: 16px;
    padding: 4px 14px;
    font-size: 0.95em;
    margin-bottom: 8px;
    margin-right: 8px;
}

/* Titres des sections */
.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1976D2;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #1976D2;
}

/* Style des graphiques */
.stPlotlyChart {
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

/* Styles spécifiques à Streamlit pour l'alignement */
.stButton>button {margin-top:0;}
.stTextInput>div>div>input {font-size:1em;}
</style>
''', unsafe_allow_html=True)

# Initialisation de la session pour le chat
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'conversation_context' not in st.session_state:
    st.session_state['conversation_context'] = {}

# Fonction pour générer un exemple de graphique
def generate_sample_plot():
    # Exemple de données pour le graphique
    data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
        'Ventes': [28, 34, 32, 30, 38, 42],
        'Objectif': [30, 30, 30, 35, 35, 40]
    })
    
    fig = px.line(data, x='Mois', y=['Ventes', 'Objectif'], 
                  title='Ventes mensuelles vs Objectifs',
                  labels={'value': 'Montant', 'variable': 'Légende'},
                  color_discrete_sequence=['#1976D2', '#FF5722'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig

# --- Titre centré ---
st.markdown('<h1 style="text-align:center;margin-bottom:30px;">Stream Digital Twin</h1>', unsafe_allow_html=True)

# --- Mise en page principale ---
main_container = st.container()

with main_container:
    
    has_charts = 'generated_charts' in st.session_state and st.session_state['generated_charts']

    if has_charts:
        # Deux colonnes si des graphiques sont présents
        col_graph, col_chat = st.columns([0.6, 0.4])
    else:
        # Une seule colonne pour le chat si aucun graphique
        col_chat = st.columns([1])[0] # Crée une seule colonne qui prend toute la largeur
        col_graph = None # Il n'y a pas de colonne de graphique

    # --- Colonne de gauche : Graphiques (conditionnelle) ---
    if col_graph:
        with col_graph:
            st.markdown('<div class="section-title">📊 Tableau de bord analytique</div>', unsafe_allow_html=True)
            for chart_json_str in st.session_state['generated_charts']:
                try:
                    fig = pio.from_json(chart_json_str)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erreur lors de l'affichage du graphique: {e}\nJSON reçu: {chart_json_str}")
    
    # --- Colonne de droite : Chat ---
    with col_chat:
        st.markdown('<div class="section-title">💬 Assistant IA</div>', unsafe_allow_html=True)
        
        # Conteneur pour les messages du chat
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Afficher l'historique des messages
            for msg in st.session_state['messages']:
                if msg['role'] == 'user':
                    st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Zone de saisie
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        with st.form(key='ask_form', clear_on_submit=True):
            question = st.text_input("Posez votre question...", "", key='input_msg', label_visibility='collapsed')
            col1, col2 = st.columns([8, 1])
            with col2:
                submit = st.form_submit_button("▶", use_container_width=True)
            with col1:
                st.write("")  # espace pour alignement
        st.markdown('</div>', unsafe_allow_html=True)

# --- Logique d'ajout des messages ---
if submit and question.strip():
    st.session_state['messages'].append({'role': 'user', 'content': question})
    
    try:
        response = requests.post(
            'http://localhost:8000/ask',
            json={
                'question': question,
                'history': st.session_state['messages'],
                'conversation_context': st.session_state['conversation_context']
            },
            timeout=15
        )
        response.raise_for_status()  # Lève une exception pour les codes d'état HTTP 4xx/5xx
        data = response.json()


        st.session_state['messages'].append({
            'role': 'bot',
            'content': data.get('final_response', "(Aucune réponse reçue.)"), # Utiliser 'final_response' comme clé de réponse
            'image_url': data.get('image_url', None),
            'meta': data.get('meta', {})
        })

        # Gérer les graphiques générés
        generated_charts_json = data.get('generated_chart', []) # S'attendre à une liste
        if generated_charts_json:
            if 'generated_charts' not in st.session_state:
                st.session_state['generated_charts'] = []
            # Ajouter tous les nouveaux graphiques à la liste existante
            st.session_state['generated_charts'].extend(generated_charts_json)

    except Exception as e:
        st.session_state['messages'].append({'role': 'bot', 'content': f"Erreur lors de la requête au backend: {e}"})
    
    # Pour rafraîchir l'affichage
    st.rerun()


