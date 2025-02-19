# ContextGPT

**ContextGPT** is an AI-powered document retrieval and answering system. It enables users to upload documents, retrieve relevant context, and generate AI-powered responses using Ollama. The system uses **ChromaDB** as a persistent vector database for efficient document search and retrieval.

## Features
- 📂 **Upload PDFs** and store document embeddings for retrieval.
- 🔍 **Retrieve relevant context** from stored documents using ChromaDB.
- 🤖 **Generate AI-powered answers** using an Ollama-backed inference service.
- 🖥️ **Simple HTML frontend** for seamless interaction.
- 🐳 **Fully containerized with Docker** for easy deployment.

---

## Deployment Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nelabdiel/contextgpt.git
cd contextgpt
```

### **2️⃣ Install Dependencies**
Ensure Python 3.11+ is installed, then run:
```bash
pip install -r requirements.txt
```

### **3️⃣ Start Services Without Docker**
You can manually start each service by running the following in separate terminals:
```bash
cd document_service && python document_service.py
```
```bash
cd retrieval_service && python retrieval_service.py
```
```bash
cd inference_service && python inference_service.py
```
```bash
cd frontend_service && python frontend_service.py
```
Now, open your browser and go to **[http://localhost:5000](http://localhost:5000)**

### **4️⃣ Start With Docker (Recommended)**
Ensure **Docker** and **Docker Compose** are installed, then run:
```bash
docker-compose up --build
```
This will build and start all services in the background.

### **5️⃣ Access the Frontend**
Once running, open your browser and go to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🛠️ Project Structure
```
/project-root
│── docker-compose.yml        # Manages all services in Docker
│── frontend_service/         # Handles UI & routes requests to backend services
│   ├── Dockerfile
│   ├── frontend_service.py
│   ├── templates/
│   │   ├── index.html        # Updated HTML frontend
│── document_service/         # Handles PDF uploads & vector storage
│   ├── Dockerfile
│   ├── document_service.py
│   ├── uploads/              # Stores uploaded PDFs
│   ├── chroma_db/            # Persistent ChromaDB storage
│── retrieval_service/        # Retrieves relevant text from vector DB
│   ├── Dockerfile
│   ├── retrieval_service.py
│── inference_service/        # Calls Ollama for AI-generated answers
│   ├── Dockerfile
│   ├── inference_service.py
│── requirements.txt          # Shared dependencies
│── README.md                 # Project documentation
```

---

## 🖥️ API Endpoints
### 📂 **Document Service (Port 5001)**
- **Upload PDFs** → `POST http://localhost:5001/upload`
- **Check status** → `GET http://localhost:5001/status`

### 🔍 **Retrieval Service (Port 5002)**
- **Retrieve relevant text** → `POST http://localhost:5002/retrieve`

### 🤖 **Inference Service (Port 5003)**
- **Generate AI response** → `POST http://localhost:5003/ask`

### 🖥️ **Frontend Service (Port 5000)**
- **Main UI** → `GET http://localhost:5000/`

---

## 🔄 Stopping and Restarting
To stop all containers:
```bash
docker-compose down
```
To restart with fresh logs:
```bash
docker-compose up --build
```

For manual (non-Docker) deployment, stop services using `CTRL+C` in each terminal window.



