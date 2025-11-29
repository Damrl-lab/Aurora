# Aurora Course-Advisor Backend

Welcome to the Aurora Course-Advisor backend! This README will guide you through setting up, running, and contributing to the Aurora microservices pipeline.

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
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview

Aurora is an academic-advising assistant built as a retrieval-augmented generation (RAG) pipeline. It consists of modular microservices that handle intent extraction, symbolic reasoning, retrieval, and language-model-based advice.

Key goals:

* 100% accurate grounding via Prolog knowledge base
* Friendly, structured advice via DeepSeek LLM
* Deterministic, reproducible responses

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
├── common/            # Shared utilities and data models
├── data_sources/      # ETL scripts for loading courses, programs, skills
├── evaluation/        # Test suites and evaluation scripts
├── pipeline_api/      # Orchestration service wiring microservices together
├── postgresDB/        # SQL schema and migration files
├── services/
│   ├── embedding_svc/ # Embedding service for vectorization
│   ├── intent_ner/    # Intent extraction & NER microservice
│   ├── pipeline_api/  # (alias) orchestrator
│   ├── prolog_kb/     # SWI‑Prolog knowledge base REST facade
│   ├── router_api/    # Router API dispatching requests to subservices
│   ├── vector_db/     # Vector database configuration (e.g., Postgres/pgvector)
│   └── deepseek_llm/  # DeepSeek Qwen‑7B LLM microservice
├── .env               # Environment variables
├── docker-compose.yml # Docker Compose config for all services
└── README.md          # (this file)
```

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
  deepseek_llm pipeline_api embedding_svc vector_db
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
4. **vector\_db**: Vector storage (Postgres + pgvector) for course embeddings.
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

---

## Contributing

1. Fork the repository and create a feature branch.
2. Write clear commit messages and keep changes scoped.
3. Add tests for new functionality under `/evaluation`.
4. Submit a Pull Request and request review.

---

## License

This project is not currently supported by any license.
