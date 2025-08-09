# Gallery-Recommender-PublicVer
This is a public version of a production project called Artomo, infrastructures api keys are abstracted

# Artomo 🎨
AI-powered art gallery recommendation app that curates free art exhibitions based on your mood, time, and location.

---

## 📸 Preview
![Artomo Screenshot](github-media/artomo_article_image.png)
![Recommendation Flow](github-media/artomo-walkthrough.gif)

---

## 📚 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Local Dependencies](#-local-dependencies)
- [Cloud Services](#-cloud-services)
- [Project Structure](#-project-structure)
- [Installation](#-installation)

---

## ✨ Features
- 🎯 **Personalized Recommendations** — Curated art exhibitions using Retrieval-Augmented Generation (RAG) + gpt-4o model.
- 📍 **Smart Filters** — Suggests galleries based on location, exhibition dates, your current mood, reason to visit and your available time.
- 🗺️ **Map Integration** — Easily navigate to galleries with Apple Maps.
- ⚡ **Low Latency Backend** — Powered by Google Cloud Run and Qdrant vector search.
- 🗂️ **Cached Reports** — Avoids regenerating LLM output for faster performance.

---

## 🏗 Architecture
![Architecture Diagram](github-media/artomo_architecture.gif)

---

## 📷 Screenshots

**Recommendation Screen**
![Recommendation Screen](docs/images/recommendation.png)

**Exhibition Details**
![Exhibition Details](docs/images/details.png)

---

## 🛠 Tech Stack
| Layer        | Technology |
|--------------|------------|
| **Frontend** | SwiftUI (iOS) |
| **Backend**  | FastAPI, Google Cloud Run |
| **Database** | MongoDB, Qdrant |
| **AI Models**| OpenAI GPT,  vector search |
| **Infra**    | ZenML, Docker |
| **Monitor**  | CometML, Opik |

---

## Local Dependencies

| Component        | Version (min) | Notes                               |
|------------------|---------------|-------------------------------------|
| Python           | 3.11.x        | Use pyenv to manage versions        |
| Poetry           | 1.7+          | Dependency + virtualenv management  |
| Docker           | 24+           | Optional for local container runs   |
| Qdrant (local)   | 1.9+          | Run via Docker for vector store     |
| MongoDB (local)  | 6.0+          | If you use Mongo; else remove       |
| ZenML (local)    | 0.74.0        | More informatio on installation and usage here: https://docs.zenml.io |
---

## Cloud Services

| Service              | Provider  | Purpose                                   |
|----------------------|-----------|-------------------------------------------|
| Cloud Run            | GCP       | Host FastAPI inference service            |
| Cloud Tasks          | GCP       | Async job dispatch for per-exhibition gen |
| Firestore (Native)   | GCP       | Cache for exhibition reports              |
| Secret Manager       | GCP       | API keys & config                         |
| Artifact Registry    | GCP       | Container images                          |
| Qdrant (Managed/VM)  | Qdrant/GCP| Vector search (exhibitions)               |
| OpenAI API           | OpenAI    | LLM report generation                     |
| Comet/Opik (optional)| Comet/Opik| Experiment/run tracking                   |

---

## 🗂️ Project Structure

Here is the directory overview:

```bash
.
├── configs/             # Configuration file containing link to sites to be crawled
├── gallery_recommender/ # Core project package
│   ├── application/     # operations including data pre-processing, transformations and RAG logic
│   ├── domain/          # Base classes, data types 
│   ├── infrastructure/  # Cloud, monitoring and inference scripts
│   ├── model/         
├── pipelines/           # ZenML pipeline definitions for ETL and Feature Engineering
├── steps/               # ZenML Pipeline components
├── tools/               # Utility scripts
│   ├── run.py
│   ├── ml_service.py
│   ├── rag.py
│   ├── data_warehouse.py
```

---

## 🚀 Installation
> **Note:** This repository is for demonstration purposes. API keys and certain configurations have been removed.

```bash
# Clone repository
git clone https://github.com/yourusername/artomo.git
cd artomo

# Install backend dependencies
pip install -r requirements.txt

# Run the backend
uvicorn app:app --reload