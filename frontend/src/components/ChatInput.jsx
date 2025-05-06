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
    <form
      className="chat-input"
      onSubmit={e => {
        e.preventDefault();
        send();
      }}
    >
      <input
        type="text"
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder="Type a message..."
      />
      <button type="submit">Send</button>
    </form>
  );
}