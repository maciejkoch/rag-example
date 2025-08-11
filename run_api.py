#!/usr/bin/env python3
"""
Script to run the Sauce Recipe RAG API server
"""

import uvicorn
import sys
import os

def main():
    """Run the FastAPI server"""
    print("🍝 Starting Sauce Recipe RAG API Server...")
    print("📚 Loading sauce recipes and initializing RAG system...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Example query: http://localhost:8000/query?q=Jak zrobić sos czosnkowy?")
    print("❤️  Health check: http://localhost:8000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()