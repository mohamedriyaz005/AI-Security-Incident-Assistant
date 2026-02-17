# 🛡️ AI Security Incident Assistant

Intelligent AI-powered incident analysis and response assistant designed for modern Security Operations Centers (SOC).

---

## 🚀 Project Overview

**AI Security Incident Assistant** is a modular, security-focused AI platform that simulates real-world SOC incident workflows.

The system enables:

- Structured security incident intake  
- Automated risk classification  
- Intelligent response recommendations  
- API-driven architecture  
- Optional LLM & vector database integration  

Built using **FastAPI** for backend services and **Streamlit** for interactive UI.

---

## 🏗️ Architecture

User (Streamlit UI)
│
▼
FastAPI Backend (REST API)
│
▼
AI Processing Layer
├── Rule-based Engine
├── Risk Scoring Logic
└── Optional LLM Integration


---

## 🧩 Tech Stack

### 🔹 Core Framework

- FastAPI  
- Uvicorn  
- Pydantic v2  

### 🔹 UI

- Streamlit  

### 🔹 AI / ML (Optional Extensions)

- NumPy  
- OpenAI API (Optional)  
- Scikit-learn (Optional)  
- Sentence Transformers (Optional)  

### 🔹 Utilities

- Python-dotenv  
- HTTPX  
- Tenacity  
- Python-dateutil  

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Security-Incident-Assistant.git
cd AI-Security-Incident-Assistant
2️⃣ Create Virtual Environment
python -m venv venv
Activate Environment
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
This assistant supports:

Incident severity prediction

Automated triage recommendations

Structured SOC reporting

Threat classification logic

Similarity search (vector DB integration)

LLM-powered summarization (optional)

The demo version runs without external AI APIs.

