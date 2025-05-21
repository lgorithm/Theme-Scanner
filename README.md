# 📑 ThemeScanner

**ThemeScanner** is a multi-modal document processing and analysis tool that allows users to upload PDF or image files, extract content using OCR or page-level parsing, and query these documents using natural language. The system returns document-specific answers and synthesizes overarching themes across the corpus.

## 🚀 Features

* 📁 Upload and parse PDFs or images (PNG, JPG) with automatic text extraction
* 🧠 Semantic search and context-aware question answering per document
* 💬 GPT-powered multi-document theme synthesis
* 🔎 Browse, preview, and view uploaded files
* 💻 Streamlit frontend + FastAPI backend
* ⚡ Async document processing for scalable performance

## 🧩 Tech Stack

* **Frontend**: Streamlit
* **Backend**: FastAPI
* **Vector DB**: Chroma
* **LLM Models**: OpenAI GPT-4, GPT-4o-mini
* **OCR**: Tesseract
* **Embeddings**: OpenAI Embeddings
* **Frameworks**: LangChain

## 🖥️ Application Architecture

```
Streamlit UI  ---> FastAPI (File Upload, Query API)
                         |
                         |--> Document Parsing (PDF/Image)
                         |--> Chroma VectorDB (LangChain)
                         |--> Retrieval-Augmented Generation
                         |--> Theme Synthesis (LLM)
```

## 🧪 Demo Screens

* 📤 **Upload Files**: Upload PDFs or images and trigger processing.
* 💬 **Agent Chat**: Ask questions about your documents.
* 📂 **Documents Viewer**: View, preview, and explore uploaded files.

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/themescanner.git
cd themescanner
```

### 2. Create a `.env` file

```ini
# .env
OPENAI_API_KEY=your_openai_key
HOST=http://localhost:8000
```

### 3. Install dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
pip install -r requirements.txt
```

### 4. Start the backend

```bash
fastapi dev main.py
```

### 5. Start the frontend

```bash
streamlit run app.py
```

## 📦 File Structure

```text
├── backend/
│   ├── main.py               # FastAPI app entry
│   ├── query.py              # Document QA + theme synthesis
│   ├── extraction.py         # PDF/image parsing and embedding
│   ├── utils.py              # Helpers for file detection
│   └── ...
├── frontend/
│   ├── app.py                # Streamlit page router
│   ├── agent.py              # Query agent interface
│   ├── uploader.py           # File upload UI
│   ├── documents.py          # File preview interface
│   └── ...
├── uploads/                  # Uploaded files
├── chroma_langchain_db/      # Vector DB directory
└── .env
```

## 🤖 How it Works

1. **Upload** files via the Streamlit UI.
2. Backend extracts text using PyMuPDF or OCR (Tesseract), then stores chunks in Chroma.
3. Users can query the documents. Each query:

   * Retrieves relevant chunks from each document.
   * Uses OpenAI to answer per-document.
   * Synthesizes themes across all answers.
4. The answer + themes are returned in the UI.

