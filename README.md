# Enterprise RAG Pipeline

A production-style Retrieval-Augmented Generation (RAG) backend system built using FastAPI, FAISS, SentenceTransformers, and local LLMs.

This project allows users to:

* Upload documents
* Process and chunk text
* Generate embeddings
* Store vectors using FAISS
* Perform semantic search
* Ask questions about uploaded documents
* Generate AI-powered responses

---

# Features

* FastAPI async backend
* Document upload system
* Semantic retrieval using embeddings
* FAISS vector similarity search
* Local embedding model support
* Local LLM integration
* SQLite database support
* Swagger API documentation
* Modular project architecture
* Background document processing
* Resume-level GenAI project

---

# Tech Stack

## Backend

* FastAPI
* Python
* SQLAlchemy
* AsyncIO

## AI/ML

* SentenceTransformers
* FAISS
* Transformers
* DistilGPT2

## Database

* SQLite

## Testing

* Pytest
* HTTPX

---

# Project Structure

```bash
rag-pipeline/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── utils/
│
├── tests/
├── data/
├── requirements.txt
├── run.py
└── README.md
```

---

# How It Works

```text
User Uploads Document
        ↓
Text Extraction
        ↓
Chunking
        ↓
Embedding Generation
        ↓
FAISS Vector Storage
        ↓
User Query
        ↓
Semantic Retrieval
        ↓
Local LLM Response Generation
```

---

# API Endpoints

## Health Check

```http
GET /api/v1/health
```

---

## Upload Document

```http
POST /api/v1/documents/upload
```

Supported formats:

* TXT
* PDF
* DOCX
* Markdown

---

## List Documents

```http
GET /api/v1/documents
```

---

## Query Documents

```http
POST /api/v1/query
```

Example:

```json
{
  "query": "What is RAG?",
  "top_k": 5
}
```

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/ratneshsingh-dul/fastapi-rag-system.git
cd fastapi-rag-system
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Server

```bash
python run.py
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Example Workflow

1. Upload a document
2. System extracts text
3. Text is chunked
4. Embeddings are generated
5. Vectors stored in FAISS
6. Ask question
7. System retrieves relevant chunks
8. Local LLM generates answer

---

# Why This Project?

Most beginner AI projects are simple chatbot wrappers.

This project focuses on:

* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* AI backend engineering
* Scalable architecture
* Production-style design

It demonstrates practical GenAI engineering concepts used in real-world AI systems.

---

# Future Improvements

* Frontend UI
* Streaming responses
* Multi-user authentication
* Docker support
* PostgreSQL integration
* Hybrid search
* OCR support
* Cloud deployment
* Chat history memory
* Multi-document conversations

---

# Author

Ratnesh Singh

GitHub:
[https://github.com/ratneshsingh-dul](https://github.com/ratneshsingh-dul)
