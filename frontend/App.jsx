import React, { useState, useRef, useEffect, useLayoutEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [question, setQuestion] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [messages, setMessages] = useState([]); // {role: 'user'|'bot', content: string}
  const [conversationContext, setConversationContext] = useState({});
  const [lastRawResponse, setLastRawResponse] = useState(null); // Pour debug visuel
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  const handleAsk = async () => {
    if (!question.trim()) return;
    
    // Ajoute la question à l'historique
    const updatedMessages = [...messages, { role: 'user', content: question }];
    setMessages(updatedMessages);
    setImageUrl('');
    
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question, 
          history: updatedMessages,
          conversation_context: conversationContext
        })
      });
      
      const data = await res.json();
      console.log('[DEBUG] Réponse brute backend:', JSON.stringify(data, null, 2));
      setLastRawResponse(data); // Stocke la dernière réponse brute pour debug UI
      
      // Mettre à jour le contexte de conversation
      if (data.conversation_context) {
        setConversationContext(data.conversation_context);
      }
      
      console.log('[DEBUG] meta:', data.meta);
      setMessages(prev => [...prev, { role: 'bot', content: data.final_response, meta: data.meta }]);
      setImageUrl(data.image_url || '');
      setQuestion(''); // Vide le champ
    } catch (error) {
      console.error('Erreur lors de la requête:', error);
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: "Désolé, une erreur est survenue lors du traitement de votre demande." 
      }]);
    }
  };

  const scrollToBottom = () => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  };

  // Scroll après rendu du DOM pour positionner au bas
  useLayoutEffect(() => {
    scrollToBottom();
  }, [messages, imageUrl]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleAsk();
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw' }}>
      {/* Affiche la colonne image uniquement si imageUrl existe */}
      {imageUrl && (
        <div style={{ flex: 1, background: '#f5f5f5', display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'all 0.3s', height: '100%' }}>
          <img src={`http://localhost:8000${imageUrl}`} alt="Présentation" style={{ maxWidth: '90%', maxHeight: '90%', borderRadius: 12, boxShadow: '0 2px 12px #aaa' }} onLoad={scrollToBottom} />
        </div>
      )}
      {/* Layer droite : chatbot */}
      <div style={{ flex: imageUrl ? 1 : '1 1 100%', display: 'flex', flexDirection: 'column', height: '100vh', background: '#fff', width: imageUrl ? undefined : '100vw', transition: 'all 0.3s' }}>
        <div style={{ padding: '32px 48px 16px 48px', flexShrink: 0 }}>
          <h1 style={{ marginTop: 0 }}>Stream Digital Twin</h1>
        </div>
        {/* Zone d'historique des messages */}
        <div ref={containerRef} style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '0 48px 0 48px', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', background: '#fff' }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              background: msg.role === 'user' ? '#e3f2fd' : '#f0f0f0',
              color: '#222',
              borderRadius: 16,
              padding: '10px 20px',
              marginBottom: 12,
              maxWidth: '80%',
              fontSize: 18,
              whiteSpace: msg.role === 'user' ? 'pre-line' : undefined
            }}>
              {msg.role === 'bot' ? (
                <>
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                  <div style={{
                    display: 'flex', justifyContent: 'flex-end', marginTop: 8
                  }}>
                    <span style={{
                      background: msg.meta && msg.meta.use_case === 'incident_analysis' ? '#1976d2' : '#43a047',
                      color: '#fff',
                      borderRadius: 10,
                      padding: '3px 12px',
                      fontSize: 14,
                      fontWeight: 500,
                      boxShadow: '0 1px 4px #bbb',
                      marginLeft: 6
                    }}>
                      {msg.meta && msg.meta.use_case === 'incident_analysis'
                        ? `🛠️ Analyse d’incident${msg.meta.incident_id ? ' – ID: ' + msg.meta.incident_id : ''}`
                        : '💬 Chatbot générique'}
                    </span>
                  </div>
                </>
              ) : msg.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {/* Zone de saisie en bas */}
        <div style={{ display: 'flex', alignItems: 'center', padding: '16px 48px', borderTop: '1px solid #eee', background: '#fff', flexShrink: 0 }}>
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Posez votre question..."
            style={{ flex: 1, padding: 12, fontSize: 18, borderRadius: 8, border: '1px solid #ccc', marginRight: 12 }}
          />
          <button onClick={handleAsk} style={{ padding: '10px 18px', fontSize: 18, borderRadius: 8, background: '#1976d2', color: '#fff', border: 'none', cursor: 'pointer' }}>
            ➤
          </button>
        </div>

      </div>
    </div>
  );
}

export default App;
