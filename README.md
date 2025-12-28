# 🛒 E-Commerce Product Recommendation System

E-Commerce Product Recommendation is a **Generative AI–driven recommendation platform** designed to provide personalized, context-aware product suggestions for online shopping platforms. It combines **LLM reasoning**, **semantic embeddings**, and **vector similarity search** to improve user experience and conversion rates.

The application is containerized with Docker, deployed on a Kubernetes cluster (Minikube running on a GCP VM), and monitored using Prometheus and Grafana for real-time observability.

---

## 🚀 Features

- 🤖 LLM-powered product recommendations using Groq
- 🧠 Semantic understanding with Hugging Face embeddings
- 🔍 Vector-based similarity search using AstraDB
- 🔗 LangChain orchestration for retrieval + generation
- 🌐 Flask backend APIs for recommendations
- 🎨 HTML/CSS frontend for product interaction
- 🐳 Dockerized microservices
- ☸️ Kubernetes deployment using Minikube
- 📊 Real-time monitoring with Prometheus
- 📈 Interactive dashboards using Grafana
- ☁️ Cloud-hosted on GCP VM

---

## 🧱 System Architecture (High-Level)

1. User interacts with the web UI (HTML/CSS)
2. Flask backend receives user/product queries
3. LangChain coordinates retrieval + LLM reasoning
4. Hugging Face embeddings convert text to vectors
5. AstraDB performs vector similarity search
6. Groq LLM generates personalized recommendations
7. App runs inside Docker containers on Kubernetes
8. Prometheus scrapes metrics from services
9. Grafana visualizes system and application metrics

---

## 🛠️ Tech Stack

| Category | Tools |
|--------|------|
| LLM | Groq |
| Embeddings | Hugging Face |
| GenAI Framework | LangChain |
| Vector Store | AstraDB |
| Backend | Flask |
| Frontend | HTML / CSS |
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube) |
| CLI | kubectl |
| Cloud | GCP VM |
| Monitoring | Prometheus |
| Visualization | Grafana |

---

# ⚙️ Setup & Run Locally
## 1️⃣ Clone
```bash
git clone https://github.com/saadtariq-ds/e-commerce-product-recommender.git
cd e-commerce-product-recommender
```

## 2️⃣ Create virtual environment (recommended)
```bash
python -m venv ven
source venv/bin/activate   # Windows: venv\Scripts\activate
```

## 3️⃣ Install dependencies
```bash
pip install -e .
```

## 4️⃣ Run Flask backend
```bash
python app.py
```