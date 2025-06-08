import streamlit as st
import requests

st.set_page_config(page_title="Stream Digital Twin", page_icon="💬", layout="wide")

# --- CSS custom pour une UI moderne ---
st.markdown('''
<style>
.chat-container {
    max-width: 700px;
    margin: 0 auto;
    padding-bottom: 90px;
}
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
.input-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #fff;
    border-top: 1px solid #eee;
    padding: 18px 0 12px 0;
    z-index: 10;
}
.input-inner {
    max-width: 700px;
    margin: 0 auto;
    display: flex;
    gap: 8px;
}
.input-inner input {
    flex: 1;
    border-radius: 8px;
    border: 1px solid #bbb;
    padding: 10px 14px;
    font-size: 1em;
}
.input-inner button {
    background: #1976D2;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0 22px;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
}
.stButton>button {margin-top:0;}
.stTextInput>div>div>input {font-size:1em;}
</style>
''', unsafe_allow_html=True)

# --- Initialisation du contexte et de l'historique ---
if 'messages' not in st.session_state or not isinstance(st.session_state['messages'], list):
    st.session_state['messages'] = []
if 'conversation_context' not in st.session_state or not isinstance(st.session_state['conversation_context'], dict):
    st.session_state['conversation_context'] = {}

# --- Titre centré ---
st.markdown('<h1 style="text-align:center;margin-bottom:30px;">Stream Digital Twin</h1>', unsafe_allow_html=True)

# --- Zone de saisie toujours en bas ---
st.markdown('<div class="input-bar"><div class="input-inner">', unsafe_allow_html=True)
with st.form(key='ask_form', clear_on_submit=True):
    question = st.text_input("Posez votre question...", "", key='input_msg', label_visibility='collapsed')
    col1, col2 = st.columns([8,1])
    with col2:
        submit = st.form_submit_button("▶", use_container_width=True)
    with col1:
        st.write("")  # espace pour alignement
st.markdown('</div></div>', unsafe_allow_html=True)

# --- Logique d'ajout des messages ---
if submit and question.strip():
    st.session_state['messages'].append({'role': 'user', 'content': question})
    try:
        # Envoyer uniquement la question, le reste est géré par la session serveur
        response = requests.post(
            'http://localhost:8000/ask',
            json={'question': question},
            cookies=st.session_state.get('cookies', {}),  # Envoyer les cookies existants
            timeout=15
        )
        
        # Sauvegarder les cookies de la réponse
        if response.cookies:
            st.session_state['cookies'] = response.cookies.get_dict()
            
        data = response.json()
        
        # Mettre à jour l'historique avec la réponse
        st.session_state['messages'].append({
            'role': 'bot',
            'content': data.get('final_response', "(Aucune réponse reçue.)"),
            'image_url': data.get('image_url'),
            'meta': data.get('meta', {})
        })
    except Exception as e:
        st.session_state['messages'].append({'role': 'bot', 'content': "Erreur lors de la requête au backend."})

# --- Affichage du chat ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        meta = msg.get('meta', {})
        badge = ''
        if meta.get('use_case') == 'incident_analysis' and meta.get('incident_id'):
            badge = f'<span class="badge-incident">🛠️ Analyse d’incident – ID : {meta["incident_id"]}</span><br>'
        st.markdown(f'<div class="bubble-bot">{badge}{msg["content"]}</div>', unsafe_allow_html=True)
        if msg.get('image_url'):
            st.image(msg['image_url'])
st.markdown('</div>', unsafe_allow_html=True)

# --- Bouton reset conversation ---
st.button("Réinitialiser la conversation", on_click=lambda: [st.session_state.pop('messages', None), st.session_state.pop('conversation_context', None)])
