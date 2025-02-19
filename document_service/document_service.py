import os
import PyPDF2 
import chromadb  
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = Flask(__name__)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

# Extract text from PDFs
def extract_text_from_pdfs(pdf_paths):
    documents = []
    for pdf_path in pdf_paths:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            documents.append(text)
    return documents

# Split text into smaller chunks before storing in ChromaDB
def chunk_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for doc in documents:
        split_chunks = text_splitter.split_text(doc)
        chunks.extend(split_chunks)
    return chunks

# Store embeddings in ChromaDB
def store_embeddings(documents):
    # Split documents into smaller chunks
    chunks = chunk_text(documents)  
    embeddings = embedding_model.encode(chunks).tolist()
    
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embeddings[i]],
            metadatas=[{"text": chunk}]
        )
    print(f"Stored {len(chunks)} text chunks in ChromaDB.")

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist("files")
    pdf_paths = []
    for file in files:
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)
        pdf_paths.append(filepath)
    
    documents = extract_text_from_pdfs(pdf_paths)
    store_embeddings(documents)
    return jsonify({"message": "Documents added to ChromaDB."})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"documents_stored": collection.count()})

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(port=5001, debug=True)
