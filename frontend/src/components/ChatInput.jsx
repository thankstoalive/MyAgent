import React, { useState } from 'react';
import './ChatInput.css';

export default function ChatInput({ onSend }) {
  const [value, setValue] = useState('');

  const send = () => {
    const text = value.trim();
    if (!text) return;
    onSend(text);
    setValue('');
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && send()}
        placeholder="Type a message..."
      />
      <button onClick={send}>Send</button>
    </div>
  );
}