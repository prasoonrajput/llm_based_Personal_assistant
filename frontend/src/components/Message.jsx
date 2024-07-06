import React from 'react';

function Message({ text, sender }) {
  return (
    <div className={`message ${sender}`}>
      <div className="message-content">{text}</div>
    </div>
  );
}

export default Message;