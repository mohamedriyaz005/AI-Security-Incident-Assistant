🛡️ AI Security Incident Assistant
<p align="center"> Intelligent AI-powered incident analysis and response assistant for modern Security Operations Centers (SOC). </p>


🚀 Project Overview

AI Security Incident Assistant is a modular security-focused AI platform designed to simulate real-world SOC incident workflows.

The system enables:

Structured security incident intake

Automated risk classification

Intelligent response recommendations

API-driven architecture

Optional LLM & vector database integration

Built using FastAPI for backend services and Streamlit for interactive UI.

🏗️ Architecture
User (Streamlit UI)
        │
        ▼
FastAPI Backend (REST API)
        │
        ▼
AI Processing Layer
        │
        ├── Rule-based Engine
        ├── Risk Scoring Logic
        └── Optional LLM Integration

🧩 Tech Stack
Core Framework

FastAPI

Uvicorn

Pydantic v2

UI

Streamlit

AI / ML (Optional Extensions)

NumPy

OpenAI API (Optional)

Scikit-learn (Optional)

Sentence Transformers (Optional)

Utilities

Python-dotenv

HTTPX

Tenacity

Python-dateutil

📦 Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/AI-Security-Incident-Assistant.git
cd AI-Security-Incident-Assistant

2️⃣ Create Virtual Environment
python -m venv venv


Activate environment:

Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

⚡ Running the Application
▶ Start Backend Server
uvicorn main:app --reload


Backend URL:

http://127.0.0.1:8000


Swagger API Docs:

http://127.0.0.1:8000/docs

▶ Start Frontend (Streamlit)
streamlit run app.py


The browser will open automatically.

🧠 AI Capabilities

This assistant can support:

Incident severity prediction

Automated triage recommendations

Structured SOC reporting

Threat classification logic

Similarity search (with vector DB integration)

LLM-powered summarization (optional)

The demo version runs without external AI APIs.

📁 Requirements.txt
# Core Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.6.0

# UI
streamlit>=1.31.0

# AI/ML (optional - not required for demo)
# openai>=1.12.0
numpy>=1.26.4
# scikit-learn>=1.4.0
# sentence-transformers>=2.3.1

# Vector Store (optional - not required for demo)
# chromadb>=0.4.22
# faiss-cpu>=1.8.0

# LLM Framework (optional - not required for demo)
# langchain>=0.1.6
# langchain-openai>=0.0.5
# langchain-community>=0.0.17

# Utilities
python-dotenv>=1.0.1
httpx>=0.26.0
# rich>=13.7.0
tenacity>=8.2.3

# Date handling
python-dateutil>=2.8.2

🔐 Example Security Use Cases

Phishing alert classification

Malware incident triage

Suspicious login investigation

Endpoint anomaly reporting

SOC Tier-1 automation

Risk severity scoring

🛠️ Production Deployment

Run with multiple workers:

uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4


Recommended for:

Docker containerization

Cloud deployment (AWS / Azure / GCP)

Internal SOC tools

📊 Professional Highlights

✔ Clean RESTful API architecture
✔ Modular AI-ready design
✔ SOC-aligned workflow modeling
✔ Async-ready backend
✔ Extensible vector integration
✔ Production-capable deployment
