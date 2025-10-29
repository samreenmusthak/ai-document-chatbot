from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import uuid
from typing import List, Optional
import json

# Using PyPDF2 which is already installed
import PyPDF2
import io

# SIMPLE EMBEDDINGS - Using a basic approach to avoid dependency issues
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ollama for LLM
import requests
import time

app = FastAPI()

# CORS middleware to allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store document data
document_text = ""
vectorizer = None
tfidf_matrix = None
chunks = []

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file using PyPDF2"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
            
    return chunks

def create_tfidf_index(text_chunks: List[str]):
    """Create TF-IDF index from text chunks"""
    global vectorizer, tfidf_matrix, chunks
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_chunks)
    chunks = text_chunks

def get_relevant_chunks(question: str, top_k: int = 3) -> List[str]:
    """Find most relevant text chunks for the question using TF-IDF"""
    global vectorizer, tfidf_matrix, chunks
    
    if vectorizer is None:
        return []
    
    # Transform question to TF-IDF
    question_vec = vectorizer.transform([question])
    
    # Calculate cosine similarity
    similarities = cosine_similarity(question_vec, tfidf_matrix).flatten()
    
    # Get top-k most similar chunks
    top_indices = similarities.argsort()[-top_k:][::-1]
    relevant_chunks = [chunks[i] for i in top_indices if i < len(chunks)]
    
    return relevant_chunks

def ask_llm(question: str, context: str) -> str:
    """Send question and context to Ollama LLM with optimized settings"""
    try:
        # Optimized prompt for faster responses
        prompt = f"""Based on this document: {context}

Question: {question}

Answer briefly from the document:"""
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:3b',  # Change to 'llama3.1:8b' or 'llama3.2:3b' if you downloaded them
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.1,  # Less creative, more factual
                    'top_k': 20,         # Limit choices for faster response
                    'top_p': 0.7,        # Limit choices for faster response
                    'num_predict': 150   # Limit response length
                }
            },
            timeout=60  # Increased timeout
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"AI service error: {response.status_code}. Please try again."
            
    except requests.exceptions.Timeout:
        return "AI is taking too long to respond. The model might be overloaded. Please try a simpler question."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to AI service. Please make sure Ollama is running."
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Handle PDF upload"""
    global document_text
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read and process PDF
    content = await file.read()
    document_text = extract_text_from_pdf(content)
    
    # Chunk text and create TF-IDF index
    text_chunks = chunk_text(document_text)
    create_tfidf_index(text_chunks)
    
    return JSONResponse(
        content={
            "message": "PDF processed successfully", 
            "chunks_count": len(text_chunks),
            "preview": document_text[:200] + "..."
        }
    )

@app.post("/chat")
async def chat_with_document(chat_request: ChatRequest):
    """Handle chat questions"""
    global vectorizer
    
    if vectorizer is None:
        raise HTTPException(status_code=400, detail="Please upload a PDF first")
    
    # Get relevant chunks
    relevant_chunks = get_relevant_chunks(chat_request.question)
    
    if not relevant_chunks:
        return ChatResponse(answer="I couldn't find relevant information in the document to answer this question.")
    
    context = "\n\n".join(relevant_chunks)
    
    # Get answer from LLM
    answer = ask_llm(chat_request.question, context)
    
    return ChatResponse(
        answer=answer
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_ready": True}

@app.get("/test-ollama")
async def test_ollama():
    """Test endpoint to check if Ollama is responding"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:3b',
                'prompt': 'Say hello in one word',
                'stream': False
            },
            timeout=10
        )
        if response.status_code == 200:
            return {"status": "success", "response": response.json()['response']}
        else:
            return {"status": "error", "code": response.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)