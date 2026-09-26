# CloudOps AI

### Enterprise Multi-Modal Agentic AI & Cloud Intelligence Platform

CloudOps AI is an enterprise-oriented agentic AI platform designed to demonstrate secure, grounded, multi-modal AI workflows across enterprise knowledge, structured data, documents, productivity workflows, and cloud operations.

The platform combines Google ADK, Gemini, RAG, PostgreSQL, FastAPI, tenant isolation, database Row-Level Security (RLS), guarded tools, agent evaluation, and automated security regression testing.

---

## Architecture

    Web / API
         |
         v
    Root Orchestrator
       Google ADK
         |
         +----------------+----------------+----------------+
         |                |                |                |
         v                v                v                v
    Research Agent    Data Agent     Multimodal Agent   Workflow Agent
         |                |                |                |
         v                v                v                v
    RAG / Knowledge   PostgreSQL      Gemini Multimodal  Workspace Tools
                         |
                         v
                  Tenant Security
                  Authorization
                  SQL Guards
                  PostgreSQL RLS

                  Security & Evaluation
        Authorization | Prompt Guard | Audit | RLS
        RAG Evaluation | Agent Evaluation | CI
        Tenant Security Regression Testing

---

## Core Capabilities

- Multi-agent orchestration with Google ADK
- Gemini-powered reasoning and multimodal analysis
- Retrieval-Augmented Generation (RAG)
- Enterprise knowledge retrieval with source provenance
- Secure structured-data analysis
- Tenant-aware database access
- PostgreSQL Row-Level Security (RLS)
- Read-only SQL execution with security guardrails
- Prompt-injection defenses
- Role-based tool authorization
- Workspace-style read-only workflows
- Agent adversarial evaluation
- RAG retrieval and grounded-answer evaluation
- Automated tenant security regression testing
- Docker-friendly development
- GitHub Actions security validation
- FastAPI backend and OpenAPI documentation
- ADK context caching

---

## Agent Architecture

CloudOps AI uses a root orchestration agent with specialized agents for different enterprise workloads.

### Root Orchestrator

The root agent determines the appropriate specialist for each request and coordinates the final response.

### Research Agent

Handles enterprise knowledge retrieval and grounded research using the RAG layer and source-aware responses.

### Data Agent

Handles structured data analysis and read-only SQL workflows while respecting database security controls and tenant boundaries.

### Multimodal Agent

Handles image and multimodal analysis using Gemini-powered capabilities.

### Workflow Agent

Handles authorized read-only productivity and Workspace-style information retrieval workflows.

---

## Retrieval-Augmented Generation

The RAG subsystem provides grounded enterprise knowledge retrieval through:

- Document ingestion
- PDF and text document processing
- Embedding generation
- Vector retrieval
- Retrieval evaluation
- Grounded-answer evaluation
- Source-aware responses

The system is designed to reduce unsupported answers by grounding responses in retrieved enterprise knowledge.

---

## Security Architecture

Security is implemented as a layered defense rather than relying only on model instructions.

    User Request
         |
         v
    Security Context
    (user + tenant + role)
         |
         v
    Tool Authorization
         |
         v
    Tenant Authorization
         |
         v
    Prompt / Input Guard
         |
         v
    Read-Only SQL Guard
         |
         v
    PostgreSQL Row-Level Security
         |
         v
    Authorized Tenant Data

### Tenant Isolation

Tenant identity is controlled by the application security context.

The AI agent cannot select or change the authorized tenant.

Database access uses a dedicated application database role configured without superuser or RLS-bypass privileges.

PostgreSQL FORCE ROW LEVEL SECURITY policies provide database-level tenant isolation.

This creates defense in depth across:

1. Agent-level security instructions
2. Application authorization
3. Tenant-bound tools
4. SQL validation
5. PostgreSQL Row-Level Security

---

## SQL Security

Database workflows are intentionally restricted to read-only operations.

The SQL security layer includes controls for:

- SELECT / read-only enforcement
- Destructive SQL blocking
- Multiple statement blocking
- SQL comment blocking
- System schema protection
- Allowed-table validation
- Query length limits
- Query timeout
- Maximum returned rows
- Tenant context validation
- Audit logging

The application uses a dedicated database role rather than the development/admin database role for agent access.

---

## Prompt Injection Defense

CloudOps AI treats external instructions and retrieved content as untrusted data.

Security controls are designed to prevent:

- System instruction extraction
- Authorization bypass
- Destructive tool execution
- Prompt injection
- Indirect prompt injection
- Unauthorized tenant access
- Unauthorized consequential actions

Agent security is evaluated using adversarial test cases rather than relying only on static prompts.

---

## Security Evaluation

CloudOps AI includes an automated tenant security evaluation suite.

### Current Tenant Security Result

**10/10 tests passed**

**Score: 1.00**

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

---

## AI Evaluation

The platform includes evaluation for:

- Prompt-injection resistance
- Agent authorization bypass attempts
- System-instruction extraction attempts
- Consequential-action safety
- RAG retrieval quality
- Grounded answer quality
- Workflow safety
- Tenant isolation
- Tool authorization

The goal is to make AI behavior measurable and regression-testable rather than relying exclusively on manual inspection.

---

## Multimodal AI

The multimodal subsystem supports Gemini-powered visual analysis workflows.

The architecture is designed to support:

- Image understanding
- Multimodal document intelligence
- Visual reasoning
- Structured multimodal tool results
- Secure agent delegation

Multimodal functionality is integrated into the broader agent orchestration architecture rather than implemented as an isolated demo.

---

## Enterprise Workflow Architecture

The Workflow Agent uses guarded read-only tools for enterprise productivity-style workflows.

The workflow layer includes:

- Workspace-style search
- Authorization checks
- Tenant-aware access
- Read-only execution
- Workflow planning
- Consequential-action confirmation requirements

Actions with potential side effects require explicit confirmation rather than being executed automatically.

---

## Context Caching

CloudOps AI uses Google ADK context caching to reduce repeated context processing across suitable multi-turn interactions.

The runtime is designed around reusable application and agent execution components.

---

## Technology Stack

### AI / Agents

- Google Gemini
- Google ADK
- LangChain
- Agentic AI
- RAG
- Multimodal AI

### Backend

- Python 3.11+
- FastAPI
- Pydantic
- REST APIs
- OpenAPI / Swagger

### Data

- PostgreSQL
- SQL
- Vector retrieval
- Tenant-aware data access
- PostgreSQL Row-Level Security

### Security

- Role-based authorization
- Tenant isolation
- Prompt guardrails
- Read-only SQL enforcement
- Database RLS
- Audit logging
- Adversarial evaluation

### Engineering

- Docker
- Git
- GitHub Actions
- pytest
- CI security regression testing

---

## Project Structure

    cloudops-ai/
    ├── backend/
    │   └── app/
    │       ├── agents/
    │       │   ├── multimodal/
    │       │   └── workflow/
    │       ├── api/
    │       ├── data/
    │       │   └── knowledge/
    │       ├── evaluation/
    │       ├── rag/
    │       │   ├── embeddings/
    │       │   ├── ingestion/
    │       │   └── retrieval/
    │       ├── runtime/
    │       ├── security/
    │       ├── tools/
    │       │   └── workspace/
    │       └── workflows/
    ├── .github/
    │   └── workflows/
    │       └── security.yml
    ├── .env.example
    ├── .gitignore
    ├── README.md
    └── backend/requirements.txt

---

## Local Setup

### 1. Clone the repository

    git clone https://github.com/Ronakmsd/cloudops-ai.git
    cd cloudops-ai

### 2. Create a virtual environment

    python3.11 -m venv .venv
    source .venv/bin/activate

### 3. Install dependencies

    pip install -r backend/requirements.txt

### 4. Configure environment variables

    cp .env.example .env

Configure the required Google Cloud and Vertex AI values locally.

Never commit `.env`.

### 5. Run the API

    uvicorn backend.app.main:app --reload

API documentation:

    http://127.0.0.1:8000/docs

---

## Run Security Evaluation

Run the tenant security evaluation with:

    PYTHONPATH=. python -m backend.app.evaluation.tenant_security_evaluator

Expected result:

    10/10 TESTS PASSED
    SCORE: 1.00

---

## Continuous Integration

The repository includes a GitHub Actions security workflow.

The CI pipeline is designed to:

1. Start an isolated PostgreSQL environment
2. Initialize tenant-aware database security
3. Create the restricted application database role
4. Enable PostgreSQL Row-Level Security
5. Run the tenant security evaluation
6. Fail the workflow if security regression tests fail

This makes security validation part of the software development lifecycle.

---

## Engineering Principles

CloudOps AI follows several core engineering principles:

1. Security controls should be enforced by application and infrastructure layers, not only by prompts.
2. Tenant identity is server-controlled and cannot be selected by the model.
3. Agent database access is read-only.
4. Retrieved content and external instructions are treated as untrusted data.
5. AI outputs should be evaluated rather than assumed to be correct.
6. Security behavior should be continuously regression-tested.
7. Enterprise AI systems should combine model intelligence with deterministic controls.
8. Consequential actions should require explicit authorization and confirmation.
9. System behavior should remain observable through evaluation and audit signals.

---

## Project Status

CloudOps AI is an actively developed engineering project demonstrating secure enterprise agentic AI architecture, Gemini-powered multimodal workflows, RAG, tenant isolation, database security, guarded enterprise tools, and automated AI/security evaluation.

The project is designed as an engineering demonstration and does not claim production deployment or real customer usage unless explicitly documented.

---

## Author

**Ronak Bhanushali**

B.Tech Information Technology

GitHub: https://github.com/Ronakmsd

LinkedIn: https://www.linkedin.com/in/ronak-bhanushali-9a188228b
