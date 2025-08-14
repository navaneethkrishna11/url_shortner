# URL Shortener

A simple and lightweight URL shortener built with **FastAPI**.  
Supports Docker deployment or manual local running.

---

## 📦 Prerequisites
Before running, make sure you have:
- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)

---

## 🚀 Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/url-shortener.git
   cd url-shortener
2. **Build and start the container**
```bash
docker build -t url-shortener .
docker run -d -p 8000:8000 url-shortener

If using docker-compose
docker compose up --build -d
docker logs url-shorter-url-shortener-1



Running Locally (Manual)

Clone the repository

git clone https://github.com/your-username/url-shortener.git
cd url-shortener


Create & activate a virtual environment

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Run the app

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


or if using run.py:

uvicorn run:app --reload --host 0.0.0.0 --port 8000


Open in browser

API Docs: http://localhost:8000/docs

Homepage: http://localhost:8000
