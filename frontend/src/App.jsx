import React, { useState } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow.jsx';
import MessageInput from './components/MessageInput.jsx';
import './Styles/App.css';

function App() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (input) => {
    setMessages([...messages, { text: input, sender: 'user' }]);
    
    try {
      const response = await axios.post('http://localhost:5000/assistant', { input });
      const assistantResponses = await response.data.response.split('\n');
      assistantResponses.forEach(resp => {
        setMessages(prevMessages => [...prevMessages, { text: resp, sender: 'assistant' }]);
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Personal Assistant</h1>
      <ChatWindow messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;