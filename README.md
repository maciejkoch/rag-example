# Sauce Recipe RAG System

A basic Retrieval-Augmented Generation (RAG) system for sauce recipes using Python, ChromaDB, and OpenAI.

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation. It works by:

1. **Retrieving** relevant documents from a knowledge base using semantic search
2. **Augmenting** the user's query with the retrieved context
3. **Generating** a response using a language model with the additional context

## Features

- Document embedding and storage using ChromaDB with **persistent storage**
- Semantic search using OpenAI embeddings
- Answer generation using OpenAI GPT models
- Simple demo with Polish sauce recipes
- Data persistence across sessions (documents stored in `./chroma/` directory)

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
2. **Choose your mode:**
   - **API Server:** `python run_api.py` (Recommended for web access)
   - **Demo mode:** `python rag_system.py`
   - **Interactive mode:** `python interactive_demo.py`

## 📦 **Where Are Dependencies Installed?**

Unlike JavaScript's `node_modules/`, Python uses:

- **Virtual environment:** `venv/lib/python3.x/site-packages/` (recommended)
- **Global installation:** System-wide Python packages location

**Virtual environments** isolate project dependencies, similar to `node_modules` but requiring manual activation.

## How it works

1. **Document Ingestion**: Sample documents are embedded using OpenAI's `text-embedding-ada-002` model
2. **Persistent Storage**: Embeddings are stored in ChromaDB's persistent database (`./chroma/` directory)
3. **Smart Loading**: On subsequent runs, existing documents are detected and skipped (no re-embedding needed)
4. **Retrieval**: When you ask a question, the system finds the most relevant documents using semantic search
5. **Generation**: The retrieved documents are used as context for GPT-3.5-turbo to generate an answer

## Project Structure

```
python-rag/
├── rag_system.py          # Main RAG implementation (with persistent storage)
├── sample_documents.py    # Polish sauce recipes for testing
├── api.py                 # FastAPI web server
├── run_api.py            # Script to start the API server
├── interactive_demo.py    # Interactive demo script
├── setup.py              # Setup script for easy installation
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # This file
├── chroma/               # ChromaDB persistent storage (auto-created)
│   ├── chroma.sqlite3    # Main database file
│   └── [UUID]/           # Vector index files
└── venv/                 # Virtual environment
```

## Example Usage

```python
from rag_system import SimpleRAGSystem

# Initialize the system
rag = SimpleRAGSystem()

# Add your documents
documents = [
    {"id": "sauce1", "content": "Sos czosnkowy: Wymieszaj jogurt grecki z czosnkiem..."}
]
rag.add_documents(documents)

# Ask questions
answer = rag.ask_question("Jak zrobić sos czosnkowy?")
print(answer)
```

## Sample Questions

The demo includes Polish sauce recipes:

- Garlic sauce (Sos czosnkowy)
- Tomato sauce for pasta (Sos pomidorowy)
- BBQ sauce (Sos barbecue)
- Dill sauce for fish (Sos koperkowy)
- Tzatziki sauce
- Mushroom sauce (Sos pieczarkowy)
- Sweet chili sauce
- Pesto sauce
- Honey-mustard sauce (Sos musztardowo-miodowy)
- Herb yogurt sauce (Sos jogurtowo-ziołowy)

Try asking questions like:

- "Jak zrobić sos czosnkowy?" (How to make garlic sauce?)
- "Jaki sos pasuje do ryby?" (Which sauce goes with fish?)
- "Potrzebuję przepisu na sos do makaronu" (I need a pasta sauce recipe)
- "Jakie sosy są idealne do grilla?" (Which sauces are perfect for grilling?)

## Persistent Storage

The system now uses **persistent storage** for better performance and data retention:

### First Run

- Documents are embedded using OpenAI API (takes time)
- Embeddings stored in `./chroma/` directory
- Database files created automatically

### Subsequent Runs

- Existing documents detected and skipped
- **Much faster startup** (no re-embedding needed)
- Data persists between sessions
- Can add new documents without losing existing ones

### Storage Location

- **Database**: `./chroma/chroma.sqlite3` (metadata, documents, embeddings)
- **Vector Index**: `./chroma/[UUID]/` (HNSW index files for fast search)
- **Size**: Typically ~188KB for sample documents

### Benefits

- ✅ **Faster restarts** - no re-embedding of existing documents
- ✅ **Data persistence** - knowledge base survives program restarts
- ✅ **Incremental growth** - add new documents without losing old ones
- ✅ **Production ready** - suitable for building real applications

## API Usage

The project now includes a **FastAPI web server** for easy integration:

### Starting the API Server

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Start the API server
python run_api.py
```

The server will be available at:

- **Main API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative docs**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

### API Endpoints

#### `GET /query` - Query Sauce Recipes

Ask questions about sauce recipes and get AI-generated answers.

**Parameters:**

- `q` (required): Your question about sauce recipes (preferably in Polish)
- `max_results` (optional): Number of recipes to retrieve (1-10, default: 3)

**Example requests:**

```bash
# Basic query
curl "http://localhost:8000/query?q=Jak zrobić sos czosnkowy?"

# With custom result limit
curl "http://localhost:8000/query?q=Jaki sos pasuje do ryby?&max_results=5"
```

**Example response:**

```json
{
  "query": "Jak zrobić sos czosnkowy?",
  "answer": "Aby zrobić sos czosnkowy, wymieszaj 200 g jogurtu greckiego z 2 posiekanymi ząbkami czosnku...",
  "retrieved_recipes": [
    {
      "rank": 1,
      "recipe_id": "sauce1",
      "content": "Sos czosnkowy: Wymieszaj 200 g jogurtu greckiego...",
      "similarity_score": 0.9234
    }
  ],
  "total_recipes_found": 1
}
```

#### `GET /health` - Health Check

Check if the API and RAG system are working properly.

#### `GET /` - API Information

Get information about available endpoints and example queries.

### Sample Queries

Try these Polish sauce recipe questions:

- `Jak zrobić sos czosnkowy?` (How to make garlic sauce?)
- `Jaki sos pasuje do ryby?` (Which sauce goes with fish?)
- `Potrzebuję przepisu na sos do makaronu` (I need a pasta sauce recipe)
- `Jakie sosy są idealne do grilla?` (Which sauces are perfect for grilling?)
- `Jak przygotować sos pesto?` (How to prepare pesto sauce?)

## Dependencies

- `chromadb`: Vector database for storing and searching embeddings
- `openai`: OpenAI API client for embeddings and text generation
- `python-dotenv`: For loading environment variables
- `fastapi`: Modern web framework for building APIs
- `uvicorn`: ASGI server for running FastAPI applications

## Note

This is a simple educational example with **persistent storage enabled**. For production use, consider:

- Error handling and retries
- Async operations for better performance
- Document chunking for large texts
- Metadata filtering
- Cost optimization
- Security best practices
- Database backup strategies
- Storage cleanup and maintenance
