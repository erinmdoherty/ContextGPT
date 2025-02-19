from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query")  # Get the form input
    if not query:
        return "Missing query", 400

    # Send JSON data to the inference service
    response = requests.post("http://localhost:5003/ask", json={"query": query, "context": ""})
    
    if response.status_code == 200:
        return render_template("index.html", response=response.json().get("response", "No response received."))
    else:
        return f"Error: {response.text}", 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
