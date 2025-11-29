# Aurora System

Welcome to **Aurora**, an academic advising platform powered by a retrieval‑augmented generation (RAG) backend—and a forthcoming user interface. This root-level README provides a high‑level overview of the full system, development setup, and pointers to individual component READMEs.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Getting Started](#getting-started)
4. [Backend](#backend)
5. [Frontend (UI)](#frontend-ui)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Overview

Aurora is a modular framework designed to help students select and plan courses using a combination of symbolic reasoning (via Prolog), vector retrieval, and language‑model explanations (via a distilled Qwen‑7B LLM). The system currently supports:

* **Backend services** (Aurora pipeline and subcomponents) for intent extraction, eligibility checks, and course recommendations.
* **Future Frontend** to deliver a web interface where students can interact with Aurora.

Key features:

* Deterministic, reproducible recommendations
* 100% accurate grounding through Prolog KB
* Clear, friendly advice from DeepSeek LLM

---

## Repository Structure

```
/                      # Root of Course-Advisor
├── backend/           # Microservices pipeline (current focus)
├── frontend/          # Web UI (in progress)
├── .gitignore
└── README.md          # (this file)
```

* **backend/**: All API, RAG services, Prolog KB, and evaluation code. See `backend/README.md` for detailed setup.
* **frontend/**: Placeholder for the React/Streamlit/Vue UI project. Coming soon!

---

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/course-advisor.git
   cd course-advisor
   ```

2. **Explore the Backend**
   Follow detailed instructions in `backend/README.md` to get the microservices running via Docker.

3. **UI Development**
   The `frontend/` folder will host the web application. Instructions and dependencies will be added once the UI scaffold is in place.

---

## Backend

The backend is a collection of FastAPI microservices, a Postgres/pgvector database, and a SWI‑Prolog knowledge base. It orchestrates:

* **Intent Extraction & NER**
* **Prolog-based Eligibility & Planning**
* **Vector Embeddings & Retrieval**
* **DeepSeek LLM Advice**

For full details and commands, see:

> 📄 [`backend/README.md`](backend/README.md)

---

## Frontend (UI)

A user-facing application is under development. The UI will:

* Provide an interactive chat or form for student queries
* Display recommended courses, eligibility details, and planning roadmaps
* Visualize prerequisite chains and course pathways

Frontend framework and instructions will be documented here once the initial scaffold is complete.

---

## Testing

* **Backend tests** live in `backend/evaluation/`. Run:

  ```bash
  cd backend
  pytest -q
  ```
* **Frontend tests** will be added alongside UI code.

---

## Contributing

1. Fork the repo and create a feature branch (`git checkout -b feature/xyz`).
2. Make your changes, ensuring you update or add tests where applicable.
3. Commit and push to your fork.
4. Open a Pull Request, describing your changes and linking any relevant issues.

Please follow the code style and commit message guidelines outlined in `backend/README.md`.

---

## License

This project is not currently supported by any license.

