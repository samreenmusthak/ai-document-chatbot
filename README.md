# AI Document Q&A Chatbot 🤖

A full-stack web application that allows users to upload PDF documents and chat with them using AI. Built with React frontend and FastAPI backend, powered by Ollama's Llama 3.2 model.

## Features

- **PDF Document Upload** - Upload and process any PDF document
- **AI-Powered Q&A** - Ask questions about your document content using Llama 3.2
- **Real-time Chat Interface** - Beautiful, responsive chat UI
- **Smart Document Retrieval** - TF-IDF based similarity search for accurate answers
- **Spark.ai Themed UI** - Professional gradient design with orange, yellow, pink, blue, and purple colors

## Tech Stack

### Frontend
- **React** - Modern UI framework
- **Axios** - HTTP client for API calls
- **CSS3** - Custom gradients and animations

### Backend
- **FastAPI** - Modern Python web framework
- **PyPDF2** - PDF text extraction
- **scikit-learn** - TF-IDF vectorization and similarity search
- **Ollama** - Local LLM inference

### AI & ML
- **Ollama** - Model serving
- **Llama 3.2 3B** - Language model for Q&A
- **TF-IDF** - Document retrieval and chunking

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samreenmusthak/ai-document-chatbot.git
   cd ai-document-chatbot
Setup Backend

bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Setup Frontend

bash
cd ../frontend
npm install
Setup Ollama

bash
# Install Ollama (if not already installed)
brew install ollama  # On Mac

# Download the AI model
ollama pull llama3.2:3b

# Start Ollama server (keep this running)
ollama serve
Running the Application

Start Ollama (in Terminal 1)

bash
ollama serve
Start Backend (in Terminal 2)

bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
Start Frontend (in Terminal 3)

bash
cd frontend
npm start
Access the Application

Frontend: http://localhost:3000
Backend API: http://localhost:8000
Health Check: http://localhost:8000/health

Project Structure

ai-document-chatbot/
├── backend/
│   ├── app.py                 # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling with Spark.ai theme
│   │   └── ...
│   ├── public/
│   └── package.json
├── samples/
│   └── sample_document.pdf   # Test document
├── screenshots/              # Application screenshots
└── README.md

How It Works

1. Document Processing

PDF uploaded and text extracted using PyPDF2
Text split into overlapping chunks (500 characters, 50 overlap)
TF-IDF vectorization creates document embeddings
2. Question Answering

User question converted to TF-IDF vector
Cosine similarity finds most relevant text chunks
Relevant context sent to Llama 3.2 model
AI generates answer based only on document content
3. AI Integration

Uses Ollama for local model inference
Llama 3.2 3B model for fast, accurate responses
Optimized prompts for document-specific answers

UI/UX Features

Animated Gradient Background - Smooth color transitions
Glass Morphism Design - Modern translucent elements
Responsive Layout - Works on desktop and mobile
Real-time Chat - Live conversation interface
Professional Branding - Spark.ai inspired theme

API Endpoints

Backend Routes

POST /upload - Upload and process PDF document
POST /chat - Ask questions about the document
GET /health - Health check and Ollama status
GET /test-ollama - Test AI model connection

Performance Optimizations

Chunk Overlap - Maintains context across text boundaries
TF-IDF Retrieval - Fast, accurate document search
Llama 3.2 3B - Balanced performance and accuracy
Connection Timeouts - Robust error handling

Troubleshooting

Common Issues

Ollama Connection Timeout

bash
# Check if Ollama is running
ollama list

# Restart Ollama
pkill ollama
ollama serve
Port Already in Use

bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
Python Dependencies

bash
# Reinstall requirements
pip install -r requirements.txt

License

This project is created as part of an internship technical assessment.

Acknowledgments

Ollama for providing easy local LLM inference
FastAPI for the modern Python web framework
React for the frontend framework

Author,
Samreen Musthak
