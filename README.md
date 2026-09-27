# CloudOps AI

### Enterprise Agentic AI & Cloud Intelligence Platform

**Google ADK · Gemini · Multi-Agent Orchestration · RAG · Multimodal AI · PostgreSQL RLS · Tenant Isolation · Cloud Run**

CloudOps AI is an enterprise-oriented Agentic AI platform designed to demonstrate how AI agents can reason across enterprise data, knowledge, documents, and workflows while remaining constrained by deterministic application, database, and infrastructure security controls.

The platform combines **Google ADK, Gemini, Retrieval-Augmented Generation (RAG), multimodal AI, PostgreSQL, Cloud SQL, PostgreSQL Row-Level Security (RLS), tenant-bound tools, SQL validation, prompt/input guards, agent evaluation, and automated security regression testing.**

> **Core engineering principle:** Model intelligence should be combined with deterministic application, database, and infrastructure controls.

---

## 🚀 Live Demo

### Public Application

https://cloudops-ai-frontend-xf6sboo7fa-uc.a.run.app

### Backend

https://cloudops-ai-xf6sboo7fa-uc.a.run.app

The deployed demonstration validates the complete browser-to-database path:

    React / Vite Frontend
             │
             ▼
    Google Cloud Run
             │
             ▼
       Google ADK API
             │
             ▼
      Root Orchestrator
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
    Research Data Multimodal
             │
             ▼
      Tenant Guarded SQL
             │
             ▼
      Cloud SQL / PostgreSQL
             │
             ▼
       PostgreSQL RLS
             │
             ▼
      Authorized Tenant Data

A Workflow Agent provides guarded read-only enterprise workflow capabilities.

The public frontend has been validated through an actual browser request against the deployed backend.

---

# 🎯 What CloudOps AI Demonstrates

CloudOps AI focuses on a practical enterprise AI engineering problem:

> **How can an AI system reason across enterprise information without allowing the model itself to become the authorization boundary?**

The architecture addresses this through defense in depth:

    Model Intelligence
           +
    Agent Orchestration
           +
    Application Authorization
           +
    Tenant-Bound Tools
           +
    SQL Validation
           +
    Database Enforcement
           +
    Automated Evaluation

Instead of relying exclusively on prompts, security controls are enforced across the application, tool, SQL, and database layers.

---

# ⭐ Engineering Highlights

| Area | Implementation |
|---|---|
| Agent framework | Google ADK |
| Foundation model | Google Gemini |
| Agent architecture | Root orchestrator + 4 specialist agents |
| Knowledge | RAG + embeddings + vector retrieval |
| Structured data | PostgreSQL / Cloud SQL |
| Tenant isolation | PostgreSQL Row-Level Security |
| Database access | Tenant-bound read-only SQL |
| SQL security | Tenant SQL validation + query guardrails |
| AI security | Prompt/input guards + tool authorization |
| Multimodal | Gemini-powered visual analysis |
| Evaluation | Security, tenant, RAG, grounded, workflow, adversarial evaluation |
| Frontend | React + Vite |
| Frontend serving | Nginx + Cloud Run |
| Backend runtime | Google ADK API + Cloud Run |
| CI | GitHub Actions security regression testing |
| Secrets | Google Secret Manager |
| Containerization | Docker |

---

# 🏗️ System Architecture

    ┌─────────────────────────┐
    │     React / Vite UI     │
    │        Cloud Run        │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │     Google ADK API      │
    │       Cloud Run         │
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │    Root Orchestrator    │
    │   cloudops_root_agent   │
    └────────────┬────────────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
    Research    Data    Multimodal
      Agent     Agent      Agent
       │         │
       │         ▼
       │   Tenant Guarded SQL
       │         │
       │         ▼
       │  Cloud SQL / PostgreSQL
       │         │
       │         ▼
       │ PostgreSQL Row-Level
       │      Security
       │         │
       │         ▼
       │ Authorized Tenant Data
       │
       └───────────────┐
                       ▼
                Workflow Agent
                 Read-Only
                 Workflows

---

# 🤖 Agent Architecture

CloudOps AI uses a root orchestration agent with specialized agents for different enterprise workloads.

## Root Orchestrator

The root agent determines the appropriate specialist based on the actual intent of the request and coordinates the final response.

Structured database requests are routed to the Data Agent rather than being handled by unrelated research or workflow agents.

## Research Agent

Handles enterprise knowledge retrieval and grounded research using the RAG layer and source-aware responses.

## Data Agent

Handles structured data analysis and read-only SQL workflows while respecting database security controls and tenant boundaries.

The Data Agent:

1. Inspects verified database schema information.
2. Generates read-only SQL.
3. Uses the tenant-guarded SQL tool.
4. Never accepts a user-supplied tenant ID as an authorization source.
5. Uses the server-authorized tenant context.
6. Returns only database results actually returned by the database layer.

## Multimodal Agent

Handles image and multimodal analysis using Gemini-powered capabilities.

The multimodal subsystem is integrated into the broader agent orchestration architecture rather than implemented as an isolated demo.

The deployed frontend supports direct image upload for visual analysis:

- Supported formats: PNG, JPEG, and WEBP
- Maximum upload size: 10 MB
- Backend endpoint: `/multimodal/analyze`
- Model: Gemini 2.5 Flash
- Production authentication: Application Default Credentials through the Cloud Run runtime service account
- Oversized uploads are rejected server-side with HTTP 413
- Image analysis is executed through Vertex AI and returned to the frontend

The upload limit is enforced independently by the backend rather than relying only on client-side validation.

## Workflow Agent

Handles authorized read-only productivity and Workspace-style information retrieval workflows.

Actions with potential side effects are designed to require explicit confirmation rather than being executed automatically.

---

# 🔎 Retrieval-Augmented Generation

The RAG subsystem provides grounded enterprise knowledge retrieval through:

- Document ingestion
- PDF and text document processing
- Gemini-powered embeddings
- Vector retrieval
- Retrieval evaluation
- Grounded-answer evaluation
- Source-aware responses

The RAG implementation is organized into:

    backend/app/rag/
    ├── embeddings/
    ├── ingestion/
    ├── retrieval/
    ├── service.py
    └── tool.py

The goal is to reduce unsupported answers by grounding responses in retrieved enterprise knowledge.

---

# 🔐 Security Architecture

Security is implemented as a layered defense rather than relying only on model instructions.

    User Request
         │
         ▼
    Server Security Context
    user + tenant + role
         │
         ▼
    Tool Authorization
         │
         ▼
    Tenant Authorization
         │
         ▼
    Prompt / Input Guard
         │
         ▼
    Read-Only SQL Guard
         │
         ▼
    Tenant SQL Validation
         │
         ▼
    PostgreSQL RLS
         │
         ▼
    Authorized Data

---

# 🛡️ Multi-Tenant Isolation

Tenant identity is controlled by the application security context.

The AI agent cannot select, change, or override the authorized tenant.

Tenant-scoped database queries use the server-controlled PostgreSQL setting:

    tenant_id = current_setting('app.tenant_id', true)

Literal tenant IDs are not used as the authorization mechanism.

The application uses a dedicated database role configured without superuser or RLS-bypass privileges.

PostgreSQL `FORCE ROW LEVEL SECURITY` policies provide database-level tenant isolation.

This creates defense in depth across:

1. Agent-level security instructions
2. Application authorization
3. Tenant-bound tools
4. SQL validation
5. PostgreSQL Row-Level Security

---

# 🔒 SQL Security

Database workflows are intentionally restricted to read-only operations.

The SQL security layer includes controls for:

- SELECT / read-only enforcement
- Destructive SQL blocking
- Multiple-statement blocking
- SQL comment blocking
- System schema protection
- Allowed-table validation
- Query length limits
- Query timeout
- Maximum returned rows
- Tenant context validation
- Tenant SQL validation
- Tool authorization

The application uses a dedicated database role rather than a development/admin database role for agent access.

---

# 🧠 Prompt Injection Defense

CloudOps AI treats external instructions and retrieved content as untrusted data.

Security controls are designed to defend against:

- System instruction extraction
- Authorization bypass
- Destructive tool execution
- Prompt injection
- Indirect prompt injection
- Unauthorized tenant access
- Tenant identity override attempts
- Unauthorized consequential actions

Relevant implementation components include:

    backend/app/security/
    ├── identity.py
    ├── prompt_guard.py
    ├── tenant_authorization.py
    ├── tenant_sql.py
    └── tool_authorization.py

Agent security is evaluated using adversarial test cases rather than relying only on static prompts.

---

# 🧪 Evaluation & Security Testing

CloudOps AI treats AI evaluation as an engineering discipline rather than relying exclusively on manual inspection.

The repository contains evaluation components for:

- Adversarial agent behavior
- Security regression
- Tenant security
- RAG retrieval
- Grounded answers
- Workflow behavior

Relevant evaluation components include:

    backend/app/evaluation/
    ├── adversarial_agent_evaluator.py
    ├── grounded_evaluator.py
    ├── rag_evaluator.py
    ├── security_evaluator.py
    ├── tenant_security_evaluator.py
    └── workflow_evaluator.py

---

# ✅ Security Evaluation Result

## 10/10 TESTS PASSED

### SCORE: 1.00

| Security Test | Result |
|---|---|
| Authorized tenant access | PASS |
| Cross-tenant customer isolation | PASS |
| Cross-tenant order isolation | PASS |
| Cross-tenant product isolation | PASS |
| Destructive SQL blocking | PASS |
| System schema access blocking | PASS |
| SQL comment attack blocking | PASS |
| Multiple statement blocking | PASS |
| Unknown table blocking | PASS |
| Tenant identity override blocking | PASS |

The evaluation executes through the application security path and validates tenant isolation, SQL restrictions, and authorization controls.

Run locally with:

    PYTHONPATH=. python -m backend.app.evaluation.tenant_security_evaluator

Expected result:

    10/10 TESTS PASSED
    SCORE: 1.00

---

# 🌐 Live Cloud Deployment Validation

The application has been deployed to Google Cloud Run for live engineering validation.

The validated request path is:

    Public Browser
          │
          ▼
    Cloud Run Frontend
          │
          ▼
    Cloud Run Backend
          │
          ▼
       Google ADK
          │
          ▼
      Root Agent
          │
          ▼
      Data Agent
          │
          ▼
    Tenant Guarded SQL
          │
          ▼
    Cloud SQL / PostgreSQL
          │
          ▼
      PostgreSQL RLS
          │
          ▼
    Authorized Tenant Records

## Authorized Tenant Request

A live browser request successfully executed the deployed path and returned the authorized tenant's customer records.

The validated demonstration returned customer records including:

- Diya Shah
- Anaya Joshi

## Cross-Tenant Request

A live request attempting to retrieve another tenant's customer records was rejected by the Data Agent.

The agent did not execute a cross-tenant SQL operation and explicitly refused to accept a user-provided tenant ID as an authorization mechanism.

These tests validate the deployed agent-routing and tenant-security path in the current demonstration environment.

---

# 🖥️ Frontend

The CloudOps AI frontend is implemented with React and Vite and served through Nginx on Cloud Run.

The interface provides:

- AI Assistant
- Data Intelligence
- Research
- Multimodal
- Workflows
- Root Orchestrator status
- Live Cloud Run status
- Tenant isolation status
- Security status
- Structured customer result cards
- Markdown-table response rendering
- Quick-action suggestions
- Free-form AI requests

- Direct image upload for Gemini-powered multimodal analysis

- PNG, JPEG, and WEBP image support

- 10 MB server-side upload validation
- Loading and error states

Example quick actions include:

    Show my customers
    Analyze enterprise data
    Search the knowledge base
    Analyze a document

The UI also communicates an important engineering principle:

> AI responses should be verified against authorized enterprise data and retrieved sources.

---

# ☁️ Cloud Deployment

## Backend

The backend runs on Google Cloud Run using the Google ADK API runtime.

The deployed service integrates with:

- Google Gemini
- Cloud SQL / PostgreSQL
- Secret Manager
- PostgreSQL RLS
- Tenant-aware security controls

## Frontend

The frontend is containerized with Docker and served through Nginx on Google Cloud Run.

The frontend communicates with the deployed ADK backend through the public Cloud Run service endpoint.

---

# ⚡ Context Caching

CloudOps AI uses Google ADK context caching to reduce repeated context processing across suitable multi-turn interactions.

The runtime is designed around reusable application and agent execution components.

---

# 🧰 Technology Stack

## AI / Agents

- Google Gemini
- Google ADK
- Agentic AI
- Multi-agent orchestration
- RAG
- Multimodal AI

## Frontend

- React
- Vite
- JavaScript
- HTML
- CSS
- Nginx
- Docker

## Backend

- Python 3.11+
- FastAPI
- Pydantic
- REST APIs
- OpenAPI / Swagger

## Data

- PostgreSQL
- Cloud SQL
- SQL
- Vector retrieval
- Tenant-aware data access
- PostgreSQL Row-Level Security

## Security

- Server-controlled identity context
- Role-based authorization
- Tenant isolation
- Prompt/input guards
- Read-only SQL enforcement
- Tenant SQL validation
- Tool authorization
- Database RLS
- Adversarial evaluation

## Cloud / Engineering

- Google Cloud Run
- Cloud SQL
- Secret Manager
- Docker
- Git
- GitHub Actions
- CI security regression testing

---

# 📁 Project Structure

    cloudops-ai/
    │
    ├── backend/
    │   └── app/
    │       ├── agents/
    │       │   ├── multimodal/
    │       │   ├── workflow/
    │       │   ├── data_agent.py
    │       │   ├── research_agent.py
    │       │   ├── tenant_data_agent.py
    │       │   └── agent.py
    │       │
    │       ├── api/
    │       ├── core/
    │       ├── data/
    │       │   └── knowledge/
    │       ├── evaluation/
    │       │   ├── adversarial_agent_evaluator.py
    │       │   ├── grounded_evaluator.py
    │       │   ├── rag_evaluator.py
    │       │   ├── security_evaluator.py
    │       │   ├── tenant_security_evaluator.py
    │       │   └── workflow_evaluator.py
    │       ├── rag/
    │       │   ├── embeddings/
    │       │   ├── ingestion/
    │       │   └── retrieval/
    │       ├── runtime/
    │       ├── security/
    │       │   ├── identity.py
    │       │   ├── prompt_guard.py
    │       │   ├── tenant_authorization.py
    │       │   ├── tenant_sql.py
    │       │   └── tool_authorization.py
    │       ├── tools/
    │       │   ├── workspace/
    │       │   ├── audit.py
    │       │   ├── database_schema.py
    │       │   ├── guarded_sql.py
    │       │   ├── request_tenant_sql.py
    │       │   ├── secure_sql.py
    │       │   └── tenant_data.py
    │       └── workflows/
    │
    ├── frontend/
    │   ├── src/
    │   │   ├── App.jsx
    │   │   ├── App.css
    │   │   ├── index.css
    │   │   └── main.jsx
    │   ├── Dockerfile
    │   ├── nginx.conf
    │   ├── package.json
    │   └── vite.config.js
    │
    ├── .github/
    │   └── workflows/
    │       └── security.yml
    │
    ├── .env.example
    ├── .gitignore
    ├── Dockerfile
    ├── backend/requirements.txt
    └── README.md

---

# 🛠️ Local Setup

## 1. Clone the repository

    git clone https://github.com/Ronakmsd/cloudops-ai.git
    cd cloudops-ai

## 2. Create a virtual environment

    python3.11 -m venv .venv
    source .venv/bin/activate

## 3. Install dependencies

    pip install -r backend/requirements.txt

## 4. Configure environment variables

    cp .env.example .env

Configure the required Google Cloud and Vertex AI values locally.

Never commit `.env`.

## 5. Run the API

    uvicorn backend.app.main:app --reload

API documentation:

    http://127.0.0.1:8000/docs

---

# 🧪 Run Security Evaluation

Run:

    PYTHONPATH=. python -m backend.app.evaluation.tenant_security_evaluator

Expected:

    10/10 TESTS PASSED
    SCORE: 1.00

---

# 🔄 Continuous Integration

The repository includes a GitHub Actions security workflow.

The CI pipeline is designed to:

1. Start an isolated PostgreSQL environment.
2. Initialize tenant-aware database security.
3. Create the restricted application database role.
4. Enable PostgreSQL Row-Level Security.
5. Run the tenant security evaluation.
6. Fail the workflow if security regression tests fail.

This makes security validation part of the software development lifecycle.

---

# 🧭 Engineering Principles

CloudOps AI follows several core engineering principles:

1. **Security controls should be enforced by application and infrastructure layers, not only by prompts.**

2. **Tenant identity is server-controlled and cannot be selected by the model.**

3. **Agent database access is read-only.**

4. **Retrieved content and external instructions are treated as untrusted data.**

5. **AI outputs should be evaluated rather than assumed to be correct.**

6. **Security behavior should be continuously regression-tested.**

7. **Enterprise AI systems should combine model intelligence with deterministic controls.**

8. **Consequential actions should require explicit authorization and confirmation.**

9. **System behavior should remain observable through evaluation and audit signals.**

---

# 🔐 Deployment & Production Security Notes

The current Cloud Run deployment is an engineering demonstration environment used to validate the live Agentic AI and tenant-security path.

The current demonstration identity layer uses a server-side identity mapping for controlled end-to-end testing.

This is **not intended to represent a complete production authentication system**.

A production deployment should derive user identity from a verified authentication boundary such as JWT/OIDC and bind authorization to that trusted identity before invoking tenant-scoped tools.

This distinction intentionally keeps the project accurate about what has been implemented and what remains as production hardening.

For Vertex AI access, the Cloud Run backend uses Application Default Credentials (ADC) through its runtime service account. No local `gcloud` CLI dependency is required inside the production container.

The deployed runtime service account is granted the Vertex AI User role required for Gemini inference. Local Docker validation can use mounted ADC credentials, while Cloud Run uses its managed workload identity environment.

---

# 📌 Project Status

CloudOps AI is an actively developed engineering project demonstrating:

- Secure enterprise Agentic AI architecture
- Google ADK orchestration
- Gemini-powered workflows
- Multi-agent architecture
- RAG and grounded retrieval
- Multimodal AI architecture
- Tenant-aware structured-data access
- PostgreSQL Row-Level Security
- Guarded read-only database tools
- Prompt-injection defenses
- Automated security evaluation
- GitHub Actions security regression testing
- Live Google Cloud Run validation
- Public frontend-to-backend E2E validation

### Current Validation

    ✓ Multi-agent orchestration
    ✓ Tenant-aware data access
    ✓ PostgreSQL RLS
    ✓ Read-only SQL controls
    ✓ Prompt/input security controls
    ✓ Automated security evaluation
    ✓ 10/10 security tests passed
    ✓ Cross-tenant access rejection
    ✓ Cloud Run deployment
    ✓ Public frontend deployment
    ✓ Browser → backend → database E2E validation

---

# 🔗 Repository

**GitHub**

https://github.com/Ronakmsd/cloudops-ai

---

# 👤 Author

**Ronak Bhanushali**

B.Tech Information Technology

**GitHub:**
https://github.com/Ronakmsd

**LinkedIn:**
https://www.linkedin.com/in/ronak-bhanushali-9a188228b

---

## Final Note

CloudOps AI is intentionally designed as an engineering demonstration of secure Agentic AI architecture.

The project emphasizes a principle that is especially important for enterprise AI systems:

> **Do not make the model the security boundary.**

Use model intelligence for reasoning and orchestration, while enforcing authorization, tenant isolation, data access, and security invariants through deterministic application, database, and infrastructure controls.
