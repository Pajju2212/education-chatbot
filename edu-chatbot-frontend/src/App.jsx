import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! Ask me anything about Education." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        query: input,
      });

      const botReply = res.data.response;

      setMessages([...newMessages, { sender: "bot", text: botReply }]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "bot", text: "Error connecting to server!" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Education Chatbot</div>

      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about education..."
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
