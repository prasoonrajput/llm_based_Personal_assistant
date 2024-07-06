import React, { useRef, useEffect } from 'react';
import Message from './Message';

function ChatWindow({ messages }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  return (
    <div className="chat-window">
      {messages.map((message, index) => (
        <Message key={index} text={message.text} sender={message.sender} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatWindow;