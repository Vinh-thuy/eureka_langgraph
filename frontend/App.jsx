import React, { useState, useRef, useEffect, useLayoutEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [question, setQuestion] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [messages, setMessages] = useState([]); // {role: 'user'|'bot', content: string}
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  const handleAsk = async () => {
    if (!question.trim()) return;
    // Ajoute la question à l'historique
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setImageUrl('');
    const res = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, history: messages })
    });
    const data = await res.json();
    console.log('[DEBUG] /ask response', data);
    setMessages(prev => [...prev, { role: 'bot', content: data.answer }]);
    setImageUrl(data.image_url || '');
    setQuestion(''); // Vide le champ
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
              {msg.role === 'bot' ? <ReactMarkdown>{msg.content}</ReactMarkdown> : msg.content}
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
