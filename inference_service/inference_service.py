import requests
from flask import Flask, request, jsonify
from ollama import Client

app = Flask(__name__)
ollama_client = Client(host='http://localhost:11434')

class TextProcessor:
    def __init__(self, model_name='llama3.2'):
        self.model_name = model_name
        self.client = ollama_client
        self.client.chat(model=self.model_name, messages=[
            {'role': 'system',
             'content': "You are a highly skilled and efficient assistant."}
        ])

    def generate_response(self, query: str, context: str) -> str:
        response = self.client.chat(model=self.model_name, messages=[
            {'role': 'user', 'content': f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"}
        ])
        return response['message']['content']

@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")
    retrieval_response = requests.post("http://localhost:5002/retrieve", json={"query": query, "k": 3})
    if retrieval_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve relevant text."})
    
    context = retrieval_response.json().get("context", "")
    processor = TextProcessor()
    response = processor.generate_response(query, context)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
