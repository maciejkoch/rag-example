"""
FastAPI application for Sauce Recipe RAG System
Provides REST API endpoints for querying sauce recipes
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import logging
from rag_system import SimpleRAGSystem
from sample_documents import SAMPLE_DOCUMENTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sauce Recipe RAG API",
    description="A RAG system API for Polish sauce recipes using ChromaDB and OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global RAG system instance
rag_system = None


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup"""
    global rag_system
    try:
        logger.info("Initializing Sauce Recipe RAG System...")
        
        # Check if OpenAI API key is available
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found - RAG system will be limited")
            return
            
        rag_system = SimpleRAGSystem()
        
        # Add sauce recipes to the system
        logger.info("Loading sauce recipes...")
        rag_system.add_documents(SAMPLE_DOCUMENTS)
        
        logger.info("RAG System initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        # Don't raise - let the app start anyway for health checks
        logger.warning("App starting without RAG system - some endpoints may not work")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sauce Recipe RAG API",
        "description": "Ask questions about Polish sauce recipes",
        "endpoints": {
            "query": "/query?q=your_question",
            "docs": "/docs",
            "health": "/health"
        },
        "example_queries": [
            "Jak zrobić sos czosnkowy?",
            "Jaki sos pasuje do ryby?",
            "Potrzebuję przepisu na sos do makaronu",
            "Jakie sosy są idealne do grilla?"
        ]
    }


@app.get("/query")
async def query_sauce_recipes(
    q: str = Query(..., description="Your question about sauce recipes in Polish"),
    max_results: Optional[int] = Query(3, description="Maximum number of recipes to retrieve", ge=1, le=10)
):
    """
    Query the sauce recipe knowledge base
    
    - **q**: Your question about sauce recipes (preferably in Polish)
    - **max_results**: Number of relevant recipes to retrieve (1-10, default: 3)
    
    Returns relevant sauce recipes and an AI-generated answer.
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'q' cannot be empty")
    
    try:
        logger.info(f"Processing query: {q}")
        
        # Search for relevant recipes
        search_results = rag_system.search_documents(q, n_results=max_results)
        
        if not search_results['documents'][0]:
            return JSONResponse(
                status_code=503,
                content={
                    "error": "No relevant recipes found",
                    "message": "This might be due to API quota issues or connection problems",
                    "query": q
                }
            )
        
        # Generate answer
        answer = rag_system.generate_answer(q, search_results['documents'][0])
        
        # Format response
        retrieved_recipes = []
        for i, (doc, metadata, distance) in enumerate(zip(
            search_results['documents'][0],
            search_results['metadatas'][0],
            search_results['distances'][0]
        )):
            retrieved_recipes.append({
                "rank": i + 1,
                "recipe_id": metadata.get('source', f"recipe_{i}"),
                "content": doc,
                "similarity_score": round(1 - distance, 4)  # Convert distance to similarity
            })
        
        return {
            "query": q,
            "answer": answer,
            "retrieved_recipes": retrieved_recipes,
            "total_recipes_found": len(retrieved_recipes)
        }
        
    except Exception as e:
        logger.error(f"Error processing query '{q}': {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error while processing query: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    import os
    
    # Basic health check - always return healthy if app is running
    health_info = {
        "status": "healthy",
        "app": "running",
        "message": "Sauce Recipe RAG API is running"
    }
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        health_info["openai_key"] = "missing"
        health_info["warning"] = "OpenAI API key not configured"
    else:
        health_info["openai_key"] = "configured"
    
    # Check RAG system status
    if not rag_system:
        health_info["rag_system"] = "not_initialized"
        health_info["warning"] = health_info.get("warning", "") + " RAG system not ready"
    else:
        try:
            collection_count = rag_system.collection.count()
            health_info["rag_system"] = "initialized"
            health_info["recipes_loaded"] = collection_count
        except Exception as e:
            health_info["rag_system"] = "error"
            health_info["rag_error"] = str(e)
    
    return health_info


if __name__ == "__main__":
    # Run the server
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )