# PDF RAG Chatbot

A modern PDF-based Retrieval-Augmented Generation (RAG) system with FastAPI backend, Streamlit frontend, FAISS vector storage, and Hugging Face integration.

## 🚀 Quick Start

### Option 1: Automated Scripts (Recommended)

**Terminal 1: Start Backend**
```powershell
.\start_backend.ps1
```

**Terminal 2: Start Frontend**
```powershell
.\start_frontend.ps1
```

### Option 2: Manual Setup

#### 1. Create virtual environment
```bash
cd pdf_rag_chatbot
python -m venv venv
venv\Scripts\activate      # on Windows
source venv/bin/activate   # on Linux/Mac
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Start Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

#### 4. Start Frontend (New Terminal)
```bash
# Activate virtual environment first
venv\Scripts\activate      # on Windows
streamlit run frontend/app.py
```

## 🌐 Access Points

- **🎨 Frontend Web App**: http://localhost:8501 (Streamlit UI)
- **⚡ Backend API**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs

## 🔧 Testing the API

### Upload PDF:
```bash
curl -X POST "http://127.0.0.1:8000/api/upload-pdf" -F "file=@sample.pdf"
```

### Ask Question:
```bash
curl -X POST "http://127.0.0.1:8000/api/ask" -H "Content-Type: application/json" -d '{"query":"What is this document about?"}'
```

## 📂 Project Structure

```
PDF_RAG_CHATBOT/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_manager.py
│   │   ├── query_engine.py
│   │   └── vector_store.py
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── reset_index.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── pdf_processor.py
│   ├── __init__.py
│   └── main.py
├── data/
│   └── faiss_index/
├── frontend/
│   ├── app.py
│   └── README.md
├── tests/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── PROJECT_OVERVIEW.md
```

## 🔧 Configuration

Set your Hugging Face API key in `.env`:
```
HF_API_KEY=your_huggingface_api_key_here
```

## 📖 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.