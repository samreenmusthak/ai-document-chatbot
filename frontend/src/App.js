import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_BASE = 'http://localhost:8000';

  const handleFileUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a PDF file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('Uploading...');
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadStatus('PDF processed successfully!');
      setConversation([{ type: 'system', message: 'PDF uploaded and processed. You can now ask questions about the document.' }]);
    } catch (error) {
      setUploadStatus('Upload failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleQuestionSubmit = async (event) => {
    event.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    const userQuestion = question;
    setQuestion('');

    // Add user question to conversation
    setConversation(prev => [...prev, { type: 'user', message: userQuestion }]);

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        question: userQuestion
      });

      // Add AI response to conversation
      setConversation(prev => [...prev, { 
        type: 'ai', 
        message: response.data.answer 
      }]);
    } catch (error) {
      setConversation(prev => [...prev, { 
        type: 'error', 
        message: 'Error: ' + (error.response?.data?.detail || error.message)
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        {/* Spark.ai Header */}
        <div className="spark-header">
          <h1 className="spark-title">Spark.AI</h1>
          <p className="spark-subtitle">Intelligent Document Analysis</p>
        </div>

        {/* Main Content Grid */}
        <div className="content-grid">
          {/* Left Column - Upload */}
          <div className="upload-section">
            <h2 className="section-title">
              <span>📄</span>
              Upload Document
            </h2>
            <form onSubmit={handleFileUpload}>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <button type="submit">Process Document</button>
            </form>
            {uploadStatus && <p className="status">{uploadStatus}</p>}
          </div>

          {/* Right Column - Chat */}
          <div className="chat-section">
            <h2 className="section-title">
              <span>💬</span>
              Chat with Document
            </h2>
            
            {/* Conversation Display */}
            <div className="conversation">
              {conversation.map((msg, index) => (
                <div key={index} className={`message ${msg.type}`}>
                  {msg.type === 'user' && 'You: '}
                  {msg.type === 'ai' && 'SparkAI: '}
                  {msg.type === 'system' && 'System: '}
                  {msg.type === 'error' && 'Error: '}
                  {msg.message}
                </div>
              ))}
              {loading && <div className="message system">Processing your question...</div>}
            </div>

            {/* Question Input */}
            <form onSubmit={handleQuestionSubmit} className="question-form">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask anything about your document..."
                disabled={loading}
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Processing...' : 'Ask'}
              </button>
            </form>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Upload Document</h3>
              <p>Upload any PDF document you want to analyze and ask questions about.</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>AI Processing</h3>
              <p>SparkAI processes your document and understands its content using advanced AI.</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Get Answers</h3>
              <p>Ask questions in natural language and get instant, accurate answers from your document.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;