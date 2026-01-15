# Aurora System

Welcome to **Aurora**, an academic advising platform powered by a retrieval‑augmented generation (RAG) backend (and a forthcoming user interface). This root-level README provides a high-level overview of the system, development setup, and pointers to component READMEs.
The code here presented aligns with the research described in "Aurora: Neuro-Symbolic AI Driven Advising Agent" (Quincoso Lugones et al., 2026)

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

Aurora is a modular neuro-symbolic framework that helps students select and plan courses by combining:
* **Structured retrieval (RAG)** of validated catalog facts.
* **Symbolic reasoning** via Prolog for enforcing prerequisites, credit caps, and program rules.
* **A BCNF-normalized PostgreSQL catalog** for stable program representation.
* **Instruction-tuned LLM generation** using a distilled Qwen-7B / DeepSeek model.
* **A structured Chain-of-Thought controller (5W+1H)** for grounded, concise prompts.

Aurora supports:

* Short-term scheduling
* Long-term degree planning
* Skill-aligned pathways
* Out-of-scope detection
* Natural-language explanations for verified plans

Key features:

* Deterministic, reproducible reasoning through SQL and Prolog
* Retrieval-augmented prompts (COURSE_FACT, PREREQ_CHAIN)
* Token-efficient prompting via the 5W+1H controller
* Clear, friendly LLM explanations grounded strictly in verified data

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

The backend is a collection of FastAPI microservices, a BCNF-normalized PostgreSQL catalog, and a SWI-Prolog reasoning engine, integrated through a retrieval-augmented generation (RAG) pipeline. It orchestrates:

* **Intent Extraction & NER**
* **SQL-based Retrieval** of relevant catalog facts (eligible courses, skills, prerequisites)
* **Prolog-based Validation & Planning** (prerequisites, co-requisites, credit caps, term constraints)
* **Structured Chain-of-Thought Controller (5W+1H)** for compact RAG prompt assembly
* **DeepSeek/Qwen LLM Generation** for natural-language explanations grounded strictly in retrieved evidence
  
Aurora’s backend supports short-term scheduling, long-term planning, skill-aligned pathways, and out-of-scope detection, all enforced through symbolic and relational constraints.

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

## Citation

When using this repository or referencing this work, please cite: Lorena Amanda Quincoso Lugones, Christopher Kverne, Nityam Shardakhrmin, Ana Carolina Oliveira, Agoritsa Polyzou, Christine Lisetti, Janki Bhimani "Aurora: Neuro-Symbolic AI Driven Advising Agent".

