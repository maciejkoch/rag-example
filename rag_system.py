"""
Sauce Recipe RAG (Retrieval-Augmented Generation) System
Using ChromaDB for vector storage and OpenAI for embeddings and generation
Specialized for Polish sauce recipes
"""

import os
import openai
import chromadb
from dotenv import load_dotenv
from sample_documents import SAMPLE_DOCUMENTS

# Load environment variables
load_dotenv()


class SimpleRAGSystem:
    def __init__(self):
        """Initialize the RAG system with ChromaDB and OpenAI"""
        # Set up OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Please set your OPENAI_API_KEY in a .env file")

        # Initialize OpenAI client with explicit API key
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            # Fallback for older OpenAI versions
            openai.api_key = api_key
            self.client = openai.OpenAI()

        # Set up ChromaDB with persistent storage
        self.chroma_client = chromadb.PersistentClient(path="./chroma")

        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="sauce_recipes",
            metadata={"description": "A collection of Polish sauce recipes"}
        )
        
        print("Sauce Recipe RAG System initialized successfully!")
    
    def get_embedding(self, text):
        """Get embeddings from OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def add_documents(self, documents):
        """Add documents to the ChromaDB collection"""
        print("Adding documents to the database...")

        # Check existing documents to avoid duplicates
        try:
            existing_docs = self.collection.get()
            existing_ids = set(existing_docs["ids"]) if existing_docs["ids"] else set()
        except Exception:
            existing_ids = set()

        added_count = 0
        for doc in documents:
            if doc["id"] in existing_ids:
                print(f"Document {doc['id']} already exists, skipping...")
                continue
                
            # Get embedding for the document
            embedding = self.get_embedding(doc["content"])
            if embedding:
                # Add to ChromaDB
                self.collection.add(
                    embeddings=[embedding],
                    documents=[doc["content"]],
                    metadatas=[{"source": doc["id"]}],
                    ids=[doc["id"]]
                )
                print(f"Added document: {doc['id']}")
                added_count += 1

        if added_count > 0:
            print(f"Successfully added {added_count} new documents to the database.")
        else:
            print("All documents already exist in the database.")
    
    def search_documents(self, query, n_results=3):
        """Search for relevant documents based on query"""
        print(f"Searching for: '{query}'")

        # Get embedding for the query
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            print("❌ Could not generate embedding for query (likely due to API quota or connection issues)")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results
    
    def generate_answer(self, query, context_documents):
        """Generate answer using OpenAI with retrieved context"""
        # Prepare context from retrieved documents
        context = "\n\n".join([doc for doc in context_documents])

        # Create prompt with context
        prompt = f"""Based on the following context documents, please answer the question.

Context:
{context}

Question: {query}

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return "❌ OpenAI API quota exceeded. Please check your billing and usage limits at https://platform.openai.com/account/billing"
            else:
                print(f"Error generating answer: {e}")
                return "❌ Sorry, I couldn't generate an answer due to an API error."
    
    def ask_question(self, query):
        """Main method to ask a question using RAG"""
        print(f"\n{'='*50}")
        print(f"Question: {query}")
        print(f"{'='*50}")

        # Step 1: Retrieve relevant documents
        search_results = self.search_documents(query)

        if not search_results['documents'][0]:
            return "❌ No relevant documents found. This might be due to API quota issues or connection problems."

        # Step 2: Display retrieved documents
        print("\nRetrieved documents:")
        for i, doc in enumerate(search_results['documents'][0]):
            print(f"{i+1}. {doc[:100]}...")

        # Step 3: Generate answer
        print("\nGenerating answer...")
        answer = self.generate_answer(query, search_results['documents'][0])

        print(f"\nAnswer: {answer}")
        return answer


def main():
    """Main function to demonstrate the sauce recipe RAG system"""
    print("Setting up Sauce Recipe RAG System...")

    # Initialize RAG system
    rag = SimpleRAGSystem()

    # Add sauce recipes
    rag.add_documents(SAMPLE_DOCUMENTS)

    # Example questions about sauce recipes
    questions = [
        "Jak zrobić sos czosnkowy?",
        "Jaki sos pasuje do ryby?",
        "Potrzebuję przepisu na sos do makaronu",
        "Jakie sosy są idealne do grilla?"
    ]

    # Ask questions
    for question in questions:
        rag.ask_question(question)
        input("\nPress Enter to continue to the next question...")

    print("\nSauce Recipe RAG Demo completed!")


if __name__ == "__main__":
    main()
