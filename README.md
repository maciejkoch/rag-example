# Simple RAG System

A basic Retrieval-Augmented Generation (RAG) system using Python, ChromaDB, and OpenAI.

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation. It works by:

1. **Retrieving** relevant documents from a knowledge base using semantic search
2. **Augmenting** the user's query with the retrieved context
3. **Generating** a response using a language model with the additional context

## Features

- Document embedding and storage using ChromaDB
- Semantic search using OpenAI embeddings
- Answer generation using OpenAI GPT models
- Simple demo with sample documents

## Setup

### Quick Setup (Recommended)

```bash
python setup.py
```

This will:

- Create a virtual environment (`venv/` folder)
- Install dependencies in the virtual environment
- Create a `.env` file for you

### Manual Setup

1. **Create virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**

   ```bash
   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key:**
   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Get your API key from: https://platform.openai.com/api-keys

### Running the System

1. **Activate virtual environment** (if not already activated)
2. **Run the demos:**
   - **Demo mode:** `python rag_system.py`
   - **Interactive mode:** `python interactive_demo.py`

## 📦 **Where Are Dependencies Installed?**

Unlike JavaScript's `node_modules/`, Python uses:

- **Virtual environment:** `venv/lib/python3.x/site-packages/` (recommended)
- **Global installation:** System-wide Python packages location

**Virtual environments** isolate project dependencies, similar to `node_modules` but requiring manual activation.

## How it works

1. **Document Ingestion**: Sample documents are embedded using OpenAI's `text-embedding-ada-002` model
2. **Storage**: Embeddings are stored in ChromaDB for fast similarity search
3. **Retrieval**: When you ask a question, the system finds the most relevant documents
4. **Generation**: The retrieved documents are used as context for GPT-3.5-turbo to generate an answer

## Project Structure

```
python-rag/
├── rag_system.py          # Main RAG implementation
├── sample_documents.py    # Sample data for testing
├── interactive_demo.py    # Interactive demo script
├── setup.py              # Setup script for easy installation
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Example Usage

```python
from rag_system import SimpleRAGSystem

# Initialize the system
rag = SimpleRAGSystem()

# Add your documents
documents = [
    {"id": "doc1", "content": "Your document content here..."}
]
rag.add_documents(documents)

# Ask questions
answer = rag.ask_question("What is Python?")
print(answer)
```

## Sample Questions

The demo includes sample documents about:

- Python programming language
- Machine Learning
- ChromaDB
- OpenAI GPT models
- RAG methodology

Try asking questions like:

- "What is Python programming language?"
- "How does ChromaDB work?"
- "What is Retrieval-Augmented Generation?"
- "Tell me about machine learning"

## Dependencies

- `chromadb`: Vector database for storing and searching embeddings
- `openai`: OpenAI API client for embeddings and text generation
- `python-dotenv`: For loading environment variables

## Note

This is a simple educational example. For production use, consider:

- Error handling and retries
- Async operations for better performance
- Document chunking for large texts
- Metadata filtering
- Cost optimization
- Security best practices
