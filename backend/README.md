# Aurora Backend

This README covers setup, architecture, and service orchestration for Aurora’s neuro-symbolic retrieval-augmented generation (RAG) pipeline.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Directory Structure](#directory-structure)
4. [Environment Configuration](#environment-configuration)
5. [Docker Setup & Commands](#docker-setup--commands)
6. [Components & Workflow](#components--workflow)
7. [Running Tests](#running-tests)
8. [Database Access](#database-access)
9. [Troubleshooting & Tips](#troubleshooting--tips)

---

## Project Overview

Aurora is an academic-advising assistant built as a neuro-symbolic, retrieval-augmented generation (RAG) pipeline.
The backend is composed of lightweight microservices that coordinate:

* Intent & entity extraction
* Structured retrieval from a BCNF PostgreSQL catalog
* Symbolic reasoning (SWI-Prolog) for prerequisites, co-requisites, and credit constraints
* 5W+1H Chain-of-Thought controller
* LLM generation using a distilled Qwen-7B / DeepSeek model
This is the exact system described and evaluated in “Aurora: Neuro-Symbolic AI Driven Advising Agent” (AIED/SAC’26).

---

## Prerequisites

* **Docker Engine** (>= 20.10)
* **Docker Compose** (>= 2.0)
* **Git**
* Optional: GPU with NVIDIA drivers for hardware acceleration

### Docker instructions:
* You may install  Docker by using the following link: https://docs.docker.com/desktop/
* After installation and restarting your machine, please, ensure that Docker is running on the background by opening the application.
* Then open a terminal as an Administrator, and verify its installation by doing:

```bash
docker info
```

---

## Directory Structure

```
/backend
├── data_sources/      # ETL scripts for loading courses, programs, skills
├── evaluation/        # Test suites and evaluation scripts
├── postgresDB/        # SQL schema, migrations, and data loaders
├── services/
│   ├── deepseek_llm/  # DeepSeek Qwen‑7B LLM microservice
│   ├── embedding_svc/ # Vector embeddings (future extension, currently unused)
│   ├── intent_ner/    # Intent extraction & NER microservice
│   ├── pipeline_api/  # End-to-end pipeline orchestrator
│   ├── prolog_kb/     # SWI‑Prolog knowledge base REST facade
│   ├── router_api/    # SQL retrieval & prompt builder
│   └── vector_db/     # PostgreSQL + pgvector configuration
├── docker-compose.yml # Docker Compose config for all services
└── README.md          # (this file)
```

**Note:** `embedding_svc/` exists for future work but is not part of the active RAG pipeline. Aurora's retrieval layer uses SQL + Prolog, not vector similarity.

---

## Environment Configuration

Copy and update the `.env` file in the `backend/` folder:

```bash
cp .env.example .env
# Edit .env to set MODEL_ID, database credentials, API keys, and any Prolog paths
```

---

## Docker Setup & Commands

### 1. Clean up older containers

```bash
docker compose down
```

### 2. Build core microservices

```bash
docker compose build router_api intent_ner prolog_kb
```

### 3. Start core services

```bash
docker compose up -d router_api intent_ner prolog_kb
```

### 4. DeepSeek LLM Service

* **First-time build:**

  ```bash
  docker compose up --build -d deepseek_llm
  ```
* **Subsequent launches (no rebuild):**

  ```bash
  docker compose up -d deepseek_llm
  # Any changes to server.py will auto-reload via Uvicorn
  ```

### 5. Full Pipeline Orchestration

```bash
# Restart / rebuild pipeline API:

docker compose restart pipeline_api

# Launch all services together:

docker compose up -d \
  router_api intent_ner prolog_kb \
  deepseek_llm pipeline_api vector_db
```

### 6. Logs & Monitoring

Follow logs for a given service:

```bash
docker compose logs -f <service_name>
# e.g. docker compose logs -f deepseek_llm
```

Combine multiple:

```bash
docker compose logs -f router_api intent_ner prolog_kb deepseek_llm pipeline_api
```

---

## Postman Testing

Use Postman (or any HTTP client) to hit the following endpoints:

* **RAG Component (intent\_ner)**
  Entry point for the RAG pipeline through the intent_ner service.

  ```http
  POST http://localhost:8001/recommend
  Content-Type: application/json

  {
    "q": "What classes should I take if I want to focus on Machine Learning?",
    "user_id": 6304012
  }
  ```

* **Aurora (pipeline\_api)**
  Full Aurora pipeline interaction.

  ```http
  POST http://localhost:8010/recommend
  Content-Type: application/json

  {
    "q": "What classes should I take if I want to focus on Machine Learning?",
    "user_id": 6304012
  }
  ```

* **Raw LLM (deepseek\_llm)**
  Test the LLM service directly.

  ```http
  POST http://localhost:8011/recommend_raw
  Content-Type: application/json

  {
    "q": "What courses should I take next semester to stay on track for my CS-BS degree (max 15 credits)?",
    "user_id": 6362138
  }
  ```

## Components & Workflow

1. **router\_api**: Entry point for client requests; routes to intent\_ner & downstream services.
2. **intent\_ner**: Neural-driven intent and named-entity recognition; extracts `recommend-courses` and parameters.
3. **prolog\_kb**: Symbolic reasoning over course prerequisites, eligibility, and long-term planning.
4. **vector\_db**: PostgreSQL instance (pgvector-enabled image) used for Aurora’s
   relational BCNF catalog. Stores courses, programs, skills, and prerequisite data.
5. **embedding\_svc**: Converts course descriptions into embedding vectors. This component is currently disconnected from the pipeline, but it might be useful in future implementations.
6. **pipeline\_api**: Orchestrates end-to-end pipeline: triggers retrieval, combines Prolog output, calls LLM.
7. **deepseek\_llm**: Qwen‑7B-based LLM service that formats chain‑of‑thought and final advice.

---

## Running Tests

From the `/backend` folder:

```bash
pytest -q evaluation
# Or run a specific test suite:
pytest evaluation/test_recommend_pipeline.py -vv
```

---

## Database Access

Connect to the Postgres vector\_db container:

```bash
docker compose exec vector_db psql -U postgres -d course_advisor
```

---

## Troubleshooting & Tips

* **Stale containers**: Always run `docker compose down` before builds. 
* **Model changes**: Editing `server.py` in `deepseek_llm` auto‑reloads Uvicorn (\~1s).
* **Port conflicts**: Ensure no other services occupy ports 8000–8010.
* **Prolog issues**: Check Prolog rule files under `services/prolog_kb`; use `DEBUG_PROLOG=true` in `.env`.
