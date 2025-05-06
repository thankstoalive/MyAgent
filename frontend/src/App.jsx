import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChatInput from './components/ChatInput';
import MessageList from './components/MessageList';

function App() {
  const [messages, setMessages] = useState([]);

  // Load chat history on mount
  useEffect(() => {
    axios.get('/chat/history')
      .then(res => setMessages(res.data.history || []))
      .catch(err => console.error('Failed to load history:', err));
  }, []);

  const handleSend = (text) => {
    // Append user message
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    // Send to backend
    axios.post('/chat/send', { content: text })
      .then(res => {
        const reply = res.data.reply;
        setMessages(prev => [...prev, { role: 'assistant', content: reply }]);
      })
      .catch(err => {
        console.error('Send failed:', err);
        setMessages(prev => [...prev, { role: 'assistant', content: 'Error sending message.' }]);
      });
  };

  return (
    <div>
      <h1>MyAgent Chat</h1>
      <MessageList messages={messages} />
      <ChatInput onSend={handleSend} />
    </div>
  );
}

export default App;