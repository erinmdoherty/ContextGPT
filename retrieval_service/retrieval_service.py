import os
import sqlite3
import chromadb
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Ensure retrieval connects to the same persistent ChromaDB path as document_service
# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
# Move ChromaDB to the project root
CHROMA_DB_PATH = os.path.join(BASE_DIR, "../document_service", "chroma_db") 
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")
DB_PATH = os.path.join(BASE_DIR, "../document_service", "documents.db")


def find_source_document(text_snippet):
    """Find which document contains the given text snippet."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, filename, filepath FROM documents WHERE full_text LIKE ?", (f"%{text_snippet}%",))
        result = cursor.fetchone()
    # Returns (title, filename, filepath) if found
    return result  

@app.route('/retrieve', methods=['POST'])
def retrieve_relevant_text():
    query = request.json.get("query")
    k = request.json.get("k", 3)

    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    if "metadatas" in results and results["metadatas"]:
        relevant_texts = [meta["text"] for meta in results["metadatas"][0]]

        references = []
        for text in relevant_texts:
            source = find_source_document(text)
            if source:
                title, filename, filepath = source
                references.append({"title": title, "filename": filename, "filepath": filepath, "excerpt": text})

        return jsonify({"context": relevant_texts, "references": references})

    return jsonify({"error": "No relevant documents found."})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
