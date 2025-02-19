from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query")
    if not query:
        return "Missing query", 400

    # Retrieve context & references
    retrieval_response = requests.post("http://localhost:5002/retrieve", json={"query": query, "k": 3})
    retrieval_data = retrieval_response.json()

    context = retrieval_data.get("context", [])
    # Extract document references
    references = retrieval_data.get("references", []) 

    # Ask AI model
    ai_response = requests.post("http://localhost:5003/ask", json={"query": query, "context": "\n".join(context)})
    ai_result = ai_response.json()

    return render_template("index.html", response=ai_result.get("response", "No response received."), references=references)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
