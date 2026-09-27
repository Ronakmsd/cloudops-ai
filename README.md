# CloudOps AI

### Enterprise Multi-Modal Agentic AI & Cloud Intelligence Platform

CloudOps AI is an enterprise-oriented Agentic AI platform built to demonstrate secure, grounded, and evaluation-driven AI workflows across enterprise knowledge, structured data, documents, multimodal inputs, productivity workflows, and cloud operations.

The platform combines Google ADK, Gemini, RAG, PostgreSQL, FastAPI, tenant isolation, PostgreSQL Row-Level Security (RLS), guarded tools, agent evaluation, and automated security regression testing.

The project focuses on a core engineering principle:

> Model intelligence should be combined with deterministic application, database, and infrastructure controls.

---

## Architecture

Web / API
↓
Google ADK API — Cloud Run Runtime
↓
Root Orchestrator — `cloudops_root_agent`
↓
├── Research Agent → RAG / Knowledge Base
├── Data Agent → Tenant Guarded SQL → PostgreSQL / Cloud SQL → PostgreSQL RLS
├── Multimodal Agent → Gemini Multimodal Analysis
└── Workflow Agent → Guarded Read-Only Workflows

Security & Evaluation Layer:

Security Context → Tool Authorization → Tenant Authorization → Prompt / Input Guards → Read-Only SQL Enforcement → Tenant SQL Validation → PostgreSQL RLS → Authorized Tenant Data

---

## Core Capabilities

- Multi-agent orchestration with Google ADK
- Gemini-powered reasoning
- Gemini-powered multimodal analysis
- Retrieval-Augmented Generation (RAG)
- Enterprise knowledge retrieval with source provenance
- Secure structured-data analysis
- Server-controlled tenant context
- PostgreSQL Row-Level Security (RLS)
- Read-only SQL execution with security guardrails
- Tenant-bound database tools
- Prompt-injection defenses
- Role-based tool authorization
- Workspace-style read-only workflows
- Agent adversarial evaluation
- RAG retrieval and grounded-answer evaluation
- Automated tenant security regression testing
- Docker-based development
- GitHub Actions security validation
- FastAPI backend and OpenAPI documentation
- Google ADK context caching

---

# Agent Architecture

CloudOps AI uses a root orchestration agent with specialized agents for different enterprise workloads.

## Root Orchestrator

The root agent determines the appropriate specialist based on the actual intent of the request and coordinates the final response.

Structured database requests are routed to the Data Agent rather than being handled by unrelated workflow or research agents.

## Research Agent

Handles enterprise knowledge retrieval and grounded research using the RAG layer and source-aware responses.

## Data Agent

Handles structured data analysis and read-only SQL workflows while respecting database security controls and tenant boundaries.

The Data Agent:

1. Inspects verified database schema information.
2. Generates read-only SQL.
3. Uses only the tenant-guarded SQL tool.
4. Never accepts a user-supplied tenant ID as an authorization source.
5. Uses the server-authorized tenant context.
6. Returns only database results actually returned by the database layer.

## Multimodal Agent

Handles image and multimodal analysis using Gemini-powered capabilities.

## Workflow Agent

Handles authorized read-only productivity and Workspace-style information retrieval workflows.

Actions with potential side effects are designed to require explicit confirmation rather than being executed automatically.

---

# Retrieval-Augmented Generation

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

# Security Architecture

Security is implemented as a layered defense rather than relying only on model instructions.

User Request
↓
Server Security Context (user + tenant + role)
↓
Tool Authorization
↓
Tenant Authorization
↓
Prompt / Input Guard
↓
Read-Only SQL Guard
↓
Tenant SQL Validation
↓
PostgreSQL Row-Level Security
↓
Authorized Tenant Data

## Tenant Isolation

Tenant identity is controlled by the application security context.

The AI agent cannot select, change, or override the authorized tenant.

Tenant-scoped database queries use the server-controlled PostgreSQL setting:

`tenant_id = current_setting('app.tenant_id', true)`

Literal tenant IDs are not used as the authorization mechanism.

Database access uses a dedicated application database role configured without superuser or RLS-bypass privileges.

PostgreSQL FORCE ROW LEVEL SECURITY policies provide database-level tenant isolation.

This creates defense in depth across:

1. Agent-level security instructions
2. Application authorization
3. Tenant-bound tools
4. SQL validation
5. PostgreSQL Row-Level Security

---

# SQL Security

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

The application uses a dedicated database role rather than the development/admin database role for agent access.

---

# Prompt Injection Defense

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

Agent security is evaluated using adversarial test cases rather than relying only on static prompts.

---

# Security Evaluation

CloudOps AI includes an automated tenant security evaluation suite.

## Automated Security Result

**10/10 TESTS PASSED**

**SCORE: 1.00**

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

# Live Cloud Deployment Validation

The application has been deployed to Google Cloud Run for live engineering validation.

Cloud Run
↓
Google ADK API
↓
Root Agent
↓
Data Agent
↓
Tenant Guarded SQL
↓
Cloud SQL PostgreSQL
↓
PostgreSQL RLS
↓
Authorized Tenant Data

## Live validation performed

### Authorized tenant request

A live request successfully executed the complete path:

Root Agent
↓
Data Agent
↓
Database Schema Tool
↓
Tenant Guarded SQL Tool
↓
PostgreSQL
↓
RLS
↓
Authorized tenant records

The live database query used the server-controlled tenant context rather than a literal tenant ID.

### Cross-tenant request

A live request attempting to retrieve another tenant's customer records was rejected by the Data Agent.

The agent did not execute a cross-tenant SQL operation and explicitly refused to accept a user-provided tenant ID as an authorization mechanism.

These tests validate the deployed agent-routing and tenant-security path in the current demonstration environment.

---

# AI Evaluation

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

# Multimodal AI

The multimodal subsystem supports Gemini-powered visual analysis workflows.

The architecture is designed to support:

- Image understanding
- Multimodal document intelligence
- Visual reasoning
- Structured multimodal tool results
- Secure agent delegation

Multimodal functionality is integrated into the broader agent orchestration architecture rather than implemented as an isolated demo.

---

# Enterprise Workflow Architecture

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

# Context Caching

CloudOps AI uses Google ADK context caching to reduce repeated context processing across suitable multi-turn interactions.

The runtime is designed around reusable application and agent execution components.

---

# Technology Stack

## AI / Agents

- Google Gemini
- Google ADK
- Agentic AI
- RAG
- Multimodal AI

## Backend

- Python 3.11+
- FastAPI
- Pydantic
- REST APIs
- OpenAPI / Swagger

## Data

- PostgreSQL
- SQL
- Vector retrieval
- Tenant-aware data access
- PostgreSQL Row-Level Security

## Security

- Role-based authorization
- Tenant isolation
- Prompt guardrails
- Read-only SQL enforcement
- Tenant SQL validation
- Database RLS
- Adversarial evaluation

## Engineering

- Docker
- Git
- GitHub Actions
- pytest
- CI security regression testing
- Google Cloud Run
- Cloud SQL
- Secret Manager

---

# Project Structure

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

# Local Setup

## 1. Clone the repository

`git clone https://github.com/Ronakmsd/cloudops-ai.git`

`cd cloudops-ai`

## 2. Create a virtual environment

`python3.11 -m venv .venv`

`source .venv/bin/activate`

## 3. Install dependencies

`pip install -r backend/requirements.txt`

## 4. Configure environment variables

`cp .env.example .env`

Configure the required Google Cloud and Vertex AI values locally.

Never commit `.env`.

## 5. Run the API

`uvicorn backend.app.main:app --reload`

API documentation:

`http://127.0.0.1:8000/docs`

---

# Run Security Evaluation

Run the tenant security evaluation with:

`PYTHONPATH=. python -m backend.app.evaluation.tenant_security_evaluator`

Expected result:

**10/10 TESTS PASSED**
**SCORE: 1.00**

---

# Continuous Integration

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

# Engineering Principles

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

# Deployment & Security Notes

The current Cloud Run deployment is an engineering demonstration environment used to validate the live Agentic AI and tenant-security path.

The current demonstration identity layer uses a server-side identity mapping for controlled end-to-end testing. It is not intended to represent a complete production authentication system.

A production deployment should derive user identity from a verified authentication boundary such as JWT/OIDC and bind authorization to that trusted identity before invoking tenant-scoped tools.

This distinction keeps the project honest about what has been implemented and what remains as production hardening.

---

# Project Status

CloudOps AI is an actively developed engineering project demonstrating:

- Secure enterprise Agentic AI architecture
- Google ADK orchestration
- Gemini-powered workflows
- RAG and grounded retrieval
- Multimodal AI architecture
- Tenant-aware structured-data access
- PostgreSQL Row-Level Security
- Guarded read-only database tools
- Prompt-injection defenses
- Automated security evaluation
- GitHub Actions security regression testing
- Live Google Cloud Run validation

The core Agentic AI and multi-tenant data-security path has been validated in the deployed demonstration environment.

---

# Author

**Ronak Bhanushali**

B.Tech Information Technology

GitHub: https://github.com/Ronakmsd

LinkedIn: https://www.linkedin.com/in/ronak-bhanushali-9a188228b
