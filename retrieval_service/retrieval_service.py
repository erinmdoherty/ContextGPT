import chromadb
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

@app.route('/retrieve', methods=['POST'])
def retrieve_relevant_text():
    query = request.json.get("query")
    k = request.json.get("k", 3)

    query_embedding = embedding_model.encode([query]).tolist()
    
    # Search ChromaDB for the most relevant documents
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
    if "metadatas" in results and results["metadatas"]:
        relevant_texts = [meta["text"] for meta in results["metadatas"][0]]
        return jsonify({"context": "\n".join(relevant_texts)})
    
    return jsonify({"error": "No relevant documents found."})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
