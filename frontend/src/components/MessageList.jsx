import React from 'react';
import './MessageList.css';

export default function MessageList({ messages }) {
  return (
    <ul className="message-list">
      {messages.map((msg, idx) => (
        <li key={idx} className={msg.role}>
          <strong>{msg.role === 'user' ? 'You' : 'Agent'}:</strong> {msg.content}
        </li>
      ))}
    </ul>
  );
}