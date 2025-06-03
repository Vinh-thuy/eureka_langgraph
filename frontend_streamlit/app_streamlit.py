import streamlit as st
import requests

st.set_page_config(page_title="Eureka Chatbot", page_icon="💬", layout="wide")

# Initialisation stricte du contexte et de l'historique en session (au tout début du script)
if 'messages' not in st.session_state or not isinstance(st.session_state['messages'], list):
    st.session_state['messages'] = []
if 'conversation_context' not in st.session_state or not isinstance(st.session_state['conversation_context'], dict):
    st.session_state['conversation_context'] = {}

st.title("💬 Eureka – Assistant d'analyse d'incident")


# Champ de saisie de la question
with st.form(key='ask_form', clear_on_submit=True):
    question = st.text_input("Posez votre question :", "")
    submit = st.form_submit_button("Envoyer")

# Logique classique : ajout et requête directement dans le bloc submit
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
        data = response.json()
        st.session_state['conversation_context'] = data.get('conversation_context', {})
        st.session_state['messages'].append({
            'role': 'bot',
            'content': data.get('final_response', "(Aucune réponse reçue.)"),
            'image_url': data.get('image_url', None),
            'meta': data.get('meta', {})
        })
    except Exception as e:
        st.session_state['messages'].append({'role': 'bot', 'content': "Erreur lors de la requête au backend."})

st.button("Réinitialiser la conversation", on_click=lambda: [st.session_state.pop('messages', None), st.session_state.pop('conversation_context', None)])

for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**Vous :** {msg['content']}")
    else:
        # Affichage du badge bleu si meta.incident_id présent et use_case=incident_analysis
        meta = msg.get('meta', {})
        if meta.get('use_case') == 'incident_analysis' and meta.get('incident_id'):
            st.markdown(
                f'<span style="background-color:#1976D2;color:white;padding:6px 16px;border-radius:16px;font-weight:bold;display:inline-block;">\
                🛠️ Analyse d’incident – ID : {meta["incident_id"]}\
                </span>',
                unsafe_allow_html=True
            )
        st.markdown(f"**Bot :** {msg['content']}")
        if msg.get('image_url'):
            st.image(msg['image_url'])
