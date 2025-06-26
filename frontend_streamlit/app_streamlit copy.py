




import streamlit as st
import requests
from datetime import datetime

# Configuration de base
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# Initialisation de la session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'cookies' not in st.session_state:
    st.session_state.cookies = {}

# Création des colonnes (50/50)
col1, col2 = st.columns(2)

# Colonne de gauche : Documentation
with col1:
    st.markdown("""
    # Documentation
    
    ## Liens utiles
    - [Documentation technique](#)
    - [Guide d'utilisation](#)
    - [Support](#)
    
    ## Instructions
    - Posez vos questions dans le chat à droite
    - Utilisez des termes précis pour des réponses plus pertinentes
    - N'hésitez pas à demander de l'aide à tout moment
    """)

# Colonne de droite : Chatbot
with col2:
    st.title("💬 Chatbot")
    
    # Historique des messages
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            if msg.get('image_url'):
                st.image(msg['image_url'])
    
    # Zone de saisie avec effacement automatique
    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input("Votre message", "", key="input_msg")
        submit = st.form_submit_button("Envoyer")

# Logique d'envoi et réception des messages
if submit and question.strip():
    # Ajout du message utilisateur
    user_message = {
        'role': 'user',
        'content': question
    }
    st.session_state.messages.append(user_message)
    
    # Envoi au backend
    try:
        response = requests.post(
            'http://localhost:8000/ask',
            json={'question': question},
            cookies=st.session_state.get('cookies', {}),
            timeout=15
        )
        
        # Sauvegarder les cookies de la réponse
        if response.cookies:
            st.session_state['cookies'] = response.cookies.get_dict()
            
        data = response.json()
        
        # Mettre à jour l'historique avec la réponse
        st.session_state.messages.append({
            'role': 'bot',
            'content': data.get('final_response', "(Aucune réponse reçue.)"),
            'image_url': data.get('image_url'),
            'meta': data.get('meta', {})
        })
    except Exception as e:
        st.session_state.messages.append({
            'role': 'bot', 
            'content': f"Erreur lors de la requête au backend: {str(e)}"
        })
    
    # Rechargement de la page pour afficher les nouveaux messages
    # La zone de saisie sera vide grâce à clear_on_submit=True dans le formulaire
    st.rerun()

