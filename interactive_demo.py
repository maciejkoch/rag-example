"""
Interactive demo for the RAG system
Allows users to ask custom questions
"""

from rag_system import SimpleRAGSystem
from sample_documents import SAMPLE_DOCUMENTS


def main():
    print("🤖 Welcome to the Interactive RAG Demo!")
    print("=" * 50)

    try:
        # Initialize RAG system
        print("Initializing RAG system...")
        rag = SimpleRAGSystem()

        # Add sample documents
        print("Loading sample documents...")
        rag.add_documents(SAMPLE_DOCUMENTS)

        print("\n✅ System ready! You can now ask questions.")
        print("💡 Sample topics: Python, Machine Learning, ChromaDB, "
              "OpenAI, RAG")
        print("Type 'quit' or 'exit' to stop.\n")

        while True:
            # Get user input
            question = input("🔍 Ask a question: ").strip()

            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            # Process the question
            try:
                rag.ask_question(question)
            except Exception as e:
                print(f"❌ Error processing question: {e}")

            print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print(f"❌ Error setting up RAG system: {e}")
        print("Make sure you have set your OPENAI_API_KEY in a .env file")


if __name__ == "__main__":
    main()
