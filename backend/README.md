# Aurora Backend

This README covers setup, architecture, and service orchestration for Aurora’s neuro-symbolic retrieval-augmented generation (RAG) pipeline.

---

> **New here? Start with [DEPLOYMENT.md](./DEPLOYMENT.md)** — a tested,
> step-by-step walkthrough for bringing the backend up on a fresh host,
> with every failure mode we actually hit and fixed. This README is a
> higher-level reference; `DEPLOYMENT.md` is the "here is exactly what
> to type" version.

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

* **Docker Desktop** (includes Docker Engine >= 20.10 and Docker Compose >= 2.0)
* **Git**
* **8+ GB RAM** recommended for running all services
* Optional: **NVIDIA GPU** for hardware-accelerated LLM inference (Windows/Linux only)

---

## Platform-Specific Setup

### macOS

1. **Install Docker Desktop**
   - Download from [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - Choose the correct version: **Apple Silicon (M1/M2/M3)** or **Intel**
   - Drag to Applications and launch

2. **Allocate Resources**
   - Open Docker Desktop → Settings → Resources
   - Recommended: **8 GB RAM**, **4 CPUs**, **50 GB disk**

3. **Verify Installation**
   ```bash
   docker info
   docker compose version
   ```

4. **GPU Note**: Apple Silicon Macs do not support NVIDIA GPUs. The LLM service will run on CPU (slower but functional).

### Windows

1. **Enable WSL 2** (Required for best performance)
   - Open PowerShell as Administrator:
     ```powershell
     wsl --install
     ```
   - Restart your computer when prompted

2. **Install Docker Desktop**
   - Download from [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - During installation, ensure **"Use WSL 2 instead of Hyper-V"** is checked
   - Restart when prompted

3. **Allocate Resources**
   - Open Docker Desktop → Settings → Resources → WSL Integration
   - Enable integration with your WSL distro
   - Under Resources → Advanced: **8 GB RAM**, **4 CPUs**

4. **Verify Installation** (PowerShell or Windows Terminal)
   ```powershell
   docker info
   docker compose version
   ```

5. **GPU Acceleration** (Optional - NVIDIA only)
   - Install [NVIDIA drivers](https://www.nvidia.com/Download/index.aspx)
   - Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
   - The `deepseek_llm` service will automatically use GPU if available

### Linux

1. **Install Docker Engine**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

2. **Verify Installation**
   ```bash
   docker info
   docker compose version
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

Create a `.env` file in `backend/postgresDB/` with the following variables:

**macOS / Linux (Terminal)**:
```bash
cd backend/postgresDB
cat > .env << 'EOF'
POSTGRES_DB=course_advisor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=vector_db
POSTGRES_PORT=5432
EOF
```

**Windows (PowerShell)**:
```powershell
cd backend\postgresDB
@"
POSTGRES_DB=course_advisor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=vector_db
POSTGRES_PORT=5432
"@ | Out-File -Encoding utf8 .env
```

Or manually create the file with any text editor containing:
```
POSTGRES_DB=course_advisor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=vector_db
POSTGRES_PORT=5432
```

### Per-Host Overrides (`backend/.env`)

A few `docker-compose.yml` values are environment-driven so you don't need to
edit the compose file to adapt the stack to your machine. Copy the template
and edit as needed:

```bash
cp backend/.env.example backend/.env
# edit backend/.env
```

| Variable | Default | When to change |
|----------|---------|----------------|
| `PIPELINE_API_PORT` | `8010` | Port `:8010` is already taken on your host (common on shared servers). |
| `CUDA_VISIBLE_DEVICES` | *(empty)* | Set to `-1` on hosts where `torch.cuda.is_available()` returns `True` but the GPU cannot actually be used — e.g., shared Linux servers whose NVML stub lies about GPU availability. Without this, `deepseek_llm` will take the 4-bit quantization path and crash with `No GPU found`. |

`backend/.env` is gitignored; `backend/.env.example` is committed as a
template so each host can carry its own overrides.

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

> **Pick a real `user_id` first.** The seeded database contains 100 students
> with randomly-generated ids. Endpoints that require a `user_id` will return
> `404 "No active program found for this user"` if you pass one that isn't
> in the seed. Query your instance:
>
> ```bash
> docker compose exec vector_db psql -U postgres -d course_advisor \
>   -c "SELECT user_id, program_id FROM User_Program WHERE status='active' LIMIT 5;"
> ```
>
> Replace the `user_id` in the examples below with one of those values.
> Also note: the port in the `pipeline_api` example is whatever you set
> `PIPELINE_API_PORT` to (default `8010`).

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

1. **intent\_ner**: Parses user queries to extract intent and entities (skills, semesters, credit caps).
2. **router\_api**: SQL-based retrieval from PostgreSQL; builds structured prompts with course facts.
3. **prolog\_kb**: Symbolic reasoning over prerequisites, eligibility, and long-term planning.
4. **deepseek\_llm**: Qwen‑7B-based LLM that generates chain-of-thought reasoning and natural-language advice.
5. **pipeline\_api**: Orchestrates the full pipeline: intent → retrieval → LLM.
6. **vector\_db**: PostgreSQL instance (pgvector-enabled) storing the BCNF-normalized course catalog.

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

### General Issues

| Issue | Solution |
|-------|----------|
| **Stale containers** | Run `docker compose down` before builds |
| **Model changes not reflected** | Editing `server.py` in `deepseek_llm` auto-reloads (~1s) |
| **Port conflicts** | Ensure ports 8000–8011 are free, or override via `PIPELINE_API_PORT` in `backend/.env` |
| **Prolog issues** | Check rule files in `services/prolog_kb`; set `DEBUG_PROLOG=true` |
| **`router_api` / `intent_ner` fail with `password authentication failed for user "postgres"`** | The `pgdata` volume was initialized with a different password than the one currently in `backend/postgresDB/.env`. Postgres only reads `POSTGRES_PASSWORD` on the first init. Non-destructive fix: `docker compose exec vector_db psql -U postgres -c "ALTER USER postgres WITH PASSWORD '''<password-from-.env>'''"`. Destructive fix: `docker compose down && docker volume rm backend_pgdata && docker compose up -d` (re-runs `db_init`). |
| **`/recommend` returns `"No active program found for this user"`** | The `user_id` you passed is not in the seeded data. Run the psql query in the Postman Testing section to find real ids. |
| **`deepseek_llm` crashes with `No GPU found. A GPU is needed for quantization.`** | `torch.cuda.is_available()` returned `True` but the GPU cannot actually be used. Set `CUDA_VISIBLE_DEVICES=-1` in `backend/.env`, then `docker compose up -d deepseek_llm`. |

### macOS-Specific

| Issue | Solution |
|-------|----------|
| **Docker Desktop won't start** | Reset Docker Desktop: `rm -rf ~/Library/Group\ Containers/group.com.docker` |
| **Slow performance on Apple Silicon** | Increase RAM allocation in Docker Desktop → Settings → Resources |
| **"Cannot connect to Docker daemon"** | Ensure Docker Desktop is running (check menu bar icon) |

### Windows-Specific

| Issue | Solution |
|-------|----------|
| **WSL 2 not installed** | Run `wsl --install` in PowerShell (Admin), then restart |
| **Docker Desktop won't start** | Ensure WSL 2 is enabled and Hyper-V is disabled |
| **"permission denied" errors** | Run PowerShell/Terminal as Administrator |
| **Line ending issues (CRLF)** | Configure Git: `git config --global core.autocrlf input` |
| **Path too long errors** | Enable long paths: `git config --global core.longpaths true` |
| **Slow file system in WSL** | Store project files in WSL filesystem (`/home/`) not Windows (`/mnt/c/`) |

### Checking Service Health

```bash
# Check if all containers are running
docker compose ps

# View logs for a specific service
docker compose logs -f <service_name>

# Restart a stuck service
docker compose restart <service_name>

# Full reset (removes volumes - will delete database!)
docker compose down -v
docker compose up -d
```
