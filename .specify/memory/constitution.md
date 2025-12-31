<!--
Sync Impact Report:
Version Change: None → 1.0.0 (Initial ratification)
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (5 principles)
  - Technical Standards
  - Architecture Principles
  - Spec-Kit Workflow
  - Agent Behavior Rules
  - Feature Requirements by Phase
  - Constraints
  - Success Criteria
  - Governance
Removed Sections: N/A (initial creation)
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section aligns
  ✅ .specify/templates/spec-template.md - User scenarios align with SDD principles
  ✅ .specify/templates/tasks-template.md - Task structure aligns with phase-based delivery
Follow-up TODOs: None
-->

# Evolution of Todo - Hackathon II Constitution

## Core Principles

### I. Spec-Driven Development (SDD) - Non-Negotiable

**NO manual coding allowed. Every feature MUST originate from a specification.**

- Constraint: Code cannot be written manually. Specifications must be refined until Claude Code generates correct output.
- All implementations MUST trace back to explicit specs in `/specs` folder.
- Evolution of specifications is part of the learning process—iterate on specs, not code.
- Follow the SDD loop strictly: Specify → Plan → Tasks → Implement.

**Rationale**: As AI agents become more capable, the engineer's role shifts from "syntax writer" to "system architect." This constraint forces mastery of spec-driven methodology and proper requirement articulation.

### II. Reusable Intelligence

**Build with modular, reusable components for maximum leverage.**

- Create and use Agent Skills and Subagents for common workflows.
- Develop Cloud-Native Blueprints for infrastructure automation.
- Favor composition over duplication across all phases.
- Document reusable patterns for team knowledge sharing.

**Rationale**: Reusable intelligence compounds productivity. Well-designed components reduce repetitive work and create consistent patterns across the project ecosystem.

### III. Cloud-Native Architecture

**Design for distributed systems from Phase I onwards.**

- Stateless services with no in-memory sessions—all state persists to database.
- Event-driven communication using Kafka (via Dapr) in Phase V.
- Containerized deployments using Docker and Kubernetes.
- Infrastructure as code using Helm Charts and declarative YAML.
- Horizontal scalability MUST be achievable without architectural changes.

**Rationale**: Cloud-native patterns are essential for modern production systems. Building with these principles from the start avoids costly architectural rewrites later.

### IV. AI-First Development

**Leverage AI agents as primary development tools.**

- Claude Code, OpenAI Agents SDK, and MCP are first-class development tools.
- Human role: System architect and spec author, not syntax writer.
- Use AIOps tools (kubectl-ai, kagent, Gordon) for intelligent operations.
- All code generation MUST reference specific Task IDs for traceability.
- Agent instructions in AGENTS.md and CLAUDE.md MUST be read before every session.

**Rationale**: AI-native development accelerates delivery and reduces manual toil. Proper agent guidance ensures consistent, high-quality output aligned with project standards.

### V. Progressive Complexity

**Each phase builds incrementally on previous phases.**

- NO skipping phases—each phase validates understanding before advancement.
- Feature progression: Basic → Intermediate → Advanced.
- Each phase completion provides deployable, demonstrable value.
- Phase order is immutable: Console → Web → Chatbot → Local K8s → Cloud.

**Rationale**: Progressive complexity ensures solid foundations. Skipping phases creates knowledge gaps and architectural debt that compound in later phases.

## Technical Standards

### Stack Requirements (Immutable)

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.13+ | Modern async support, type hints |
| Package Manager | UV | Latest | Fast, reliable dependency management |
| Frontend | Next.js | 16+ (App Router) | React Server Components, optimal performance |
| Backend | FastAPI | Latest | Async Python, OpenAPI auto-generation |
| ORM | SQLModel | Latest | Type-safe Pydantic + SQLAlchemy hybrid |
| Database | Neon Serverless PostgreSQL | Latest | Serverless, auto-scaling, developer-friendly |
| Auth | Better Auth | Latest | JWT-based, Next.js native |
| AI Framework | OpenAI Agents SDK | Latest | Official agentic patterns |
| MCP | Official MCP SDK | Latest | Standardized tool interface |
| Chatbot UI | OpenAI ChatKit | Latest | Pre-built conversational interface |
| Container | Docker | Latest | Industry standard containerization |
| Orchestration | Kubernetes (Minikube/DOKS) | Latest stable | Cloud-native deployment |
| Package Manager | Helm | 3.x | Kubernetes application packaging |
| Event Streaming | Kafka (via Dapr) | Latest | Event-driven architecture |
| Service Mesh | Dapr | Latest | Distributed application runtime |

### Development Toolchain (Required)

| Tool | Purpose | Phase |
|------|---------|-------|
| Claude Code | Primary code generation | All |
| Spec-Kit Plus | Specification management | All |
| kubectl-ai | AI-assisted K8s operations | IV, V |
| kagent | Advanced K8s cluster management | IV, V |
| Gordon (Docker AI) | AI-assisted Docker operations | IV, V |

### Platform Requirements

**Windows Users: Mandatory WSL 2**

- All Windows participants MUST use WSL 2 (Ubuntu 22.04 recommended).
- Native Windows development is NOT supported for this hackathon.

## Architecture Principles

### 1. Separation of Concerns

- **Frontend**: UI/UX only, no business logic.
- **Backend**: Business logic, orchestration, API endpoints.
- **MCP Server**: Tool interface layer between AI and application logic.
- **Database**: Persistent state only, no computed logic.

### 2. Stateless Services

- NO in-memory sessions—all state persists to database.
- Servers MUST be horizontally scalable.
- Conversation state stored in Neon DB, not local memory.

### 3. Event-Driven Communication (Phase V)

- Services communicate via Kafka events, not direct API calls.
- Pub/Sub pattern for decoupling producers and consumers.
- Event schema versioning for backward compatibility.

### 4. Security-First

- **JWT Authentication**: All API endpoints require valid tokens.
- **User Isolation**: Each user sees only their own data.
- **Secrets Management**: No hardcoded credentials (use Dapr/K8s secrets).
- **API Security**: Better Auth JWT integration with FastAPI middleware.

### 5. Observability

- Structured logging (JSON format preferred).
- Health check endpoints (`/health`, `/readiness`).
- Metrics-ready for Prometheus scraping (Phase V).

## Spec-Kit Workflow (Mandatory Process)

### The SDD Loop: Specify → Plan → Tasks → Implement

```
┌─────────────┐
│  SPECIFY    │  What needs to be built? (Requirements, journeys, acceptance criteria)
│  (.specify) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    PLAN     │  How will it be built? (Architecture, components, APIs, schema)
│   (.plan)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   TASKS     │  Break into atomic, testable work units (Task IDs, preconditions)
│  (.tasks)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ IMPLEMENT   │  Claude Code generates code from tasks (code must reference Task IDs)
│   (code)    │
└─────────────┘
```

### File Structure Convention

```
cloud-native-todo-hackathon/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # THIS FILE (project principles)
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── phr-template.prompt.md
│   └── scripts/
│       └── bash/
│           └── create-phr.sh
├── specs/
│   ├── overview.md                  # High-level project summary
│   ├── architecture.md              # System architecture diagrams
│   ├── features/                    # Feature specifications
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                         # API specifications
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/                    # Database specifications
│   │   └── schema.md
│   └── ui/                          # UI specifications
│       ├── components.md
│       └── pages.md
├── history/
│   ├── prompts/                     # Prompt History Records
│   │   ├── constitution/
│   │   ├── general/
│   │   └── <feature-name>/
│   └── adr/                         # Architecture Decision Records
├── AGENTS.md                        # Agent behavior instructions
├── CLAUDE.md                        # Claude Code entry point
├── frontend/
│   ├── CLAUDE.md                   # Frontend-specific guidelines
│   └── ...                         # Next.js app
├── backend/
│   ├── CLAUDE.md                   # Backend-specific guidelines
│   └── ...                         # FastAPI app
├── docker-compose.yml
└── README.md
```

### Spec Hierarchy (Conflict Resolution)

When specs conflict, this priority applies:

1. **Constitution** (this file) - Immutable principles
2. **Specify** - Requirements and acceptance criteria
3. **Plan** - Architecture and implementation approach
4. **Tasks** - Atomic work units

## Agent Behavior Rules

### What AI Agents MUST Do

✅ Read AGENTS.md and CLAUDE.md before every session.
✅ Reference Task IDs in every code commit.
✅ Update specs before proposing architecture changes.
✅ Request clarification when specs are incomplete.
✅ Follow the SDD loop: Specify → Plan → Tasks → Implement.
✅ Create Prompt History Records (PHRs) for all significant work.
✅ Suggest Architecture Decision Records (ADRs) for significant decisions.

### What AI Agents MUST NOT Do

❌ Generate code without a referenced Task ID.
❌ Modify architecture without updating plan documentation.
❌ Propose features without updating specifications.
❌ Invent requirements or "creative" implementations.
❌ Ignore acceptance criteria.
❌ Use localStorage/sessionStorage in artifacts (not supported in Claude.ai).
❌ Hardcode credentials or secrets.

## Feature Requirements by Phase

### Phase I: In-Memory Python Console App (100 points)

**Basic Level Features (Required)**:

1. Add Task (title, description)
2. Delete Task (by ID)
3. Update Task (modify details)
4. View Task List (display all tasks)
5. Mark as Complete/Incomplete (toggle status)

**Technology**: Python 3.13+, UV, Claude Code, Spec-Kit Plus

**Constraints**: No UI, no database—pure in-memory data structures.

**Success Criteria**:
- ✅ All 5 Basic Level features working in console
- ✅ Spec-driven implementation traceable
- ✅ Clean Python project structure
- ✅ CLAUDE.md and specs/ folder present

### Phase II: Full-Stack Web Application (150 points)

**Same Basic Level Features + Persistence + Multi-User**:

- RESTful API with FastAPI
- Next.js frontend with responsive UI
- Neon Serverless PostgreSQL storage
- Authentication: Better Auth with JWT
- API Security: JWT token validation, user isolation

**API Endpoints**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all user tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

**Success Criteria**:
- ✅ RESTful API fully functional
- ✅ Responsive Next.js UI deployed on Vercel
- ✅ Better Auth JWT integration working
- ✅ Multi-user data isolation verified
- ✅ Neon DB connection stable

### Phase III: AI-Powered Todo Chatbot (200 points)

**Conversational Interface for Basic Features**:

- OpenAI ChatKit UI
- OpenAI Agents SDK for AI logic
- MCP Server with Official MCP SDK (5 tools: add, list, complete, delete, update)
- Stateless chat endpoint with DB-persisted conversation state
- Natural language commands (e.g., "Reschedule my morning meetings to 2 PM")

**Database Models**:

- **Task**: user_id, id, title, description, completed, created_at, updated_at
- **Conversation**: user_id, id, created_at, updated_at
- **Message**: user_id, id, conversation_id, role, content, created_at

**MCP Tools**: add_task, list_tasks, complete_task, delete_task, update_task

**Success Criteria**:
- ✅ Conversational interface via ChatKit
- ✅ MCP Server with 5 tools operational
- ✅ Stateless chat endpoint persisting to DB
- ✅ Natural language commands working
- ✅ OpenAI Domain Allowlist configured

### Phase IV: Local Kubernetes Deployment (250 points)

**Containerize + Orchestrate**:

- Docker containers for frontend and backend (use Gordon for AI-assisted Docker ops)
- Helm Charts for deployment
- Deploy on Minikube locally
- Use kubectl-ai and kagent for AI-assisted K8s operations

**Deliverables**:

- Dockerfile for each service
- Helm chart templates
- Working deployment on Minikube
- Instructions for local setup

**Success Criteria**:
- ✅ Containers running on Minikube
- ✅ Helm Charts deployable
- ✅ kubectl-ai and kagent commands functional
- ✅ Docker AI (Gordon) used for containerization

### Phase V: Advanced Cloud Deployment (300 points)

**Part A: Advanced Features**

- ✅ Recurring Tasks (auto-reschedule)
- ✅ Due Dates & Time Reminders (browser notifications)
- ✅ Priorities & Tags/Categories (high/medium/low, work/home)
- ✅ Search & Filter (keyword search, filter by status/priority/date)
- ✅ Sort Tasks (by due date, priority, alphabetically)

**Part B: Event-Driven Architecture**

- Kafka integration (via Dapr Pub/Sub)
- Event topics: task-events, reminders, task-updates
- Microservices: Notification Service, Recurring Task Service, Audit Service

**Part C: Dapr Integration**

- Pub/Sub (Kafka abstraction)
- State Management (conversation state)
- Service Invocation (frontend ↔ backend)
- Jobs API (scheduled reminders at exact times, not cron polling)
- Secrets Management (API keys, DB credentials)

**Part D: Cloud Deployment**

- Deploy on Azure AKS / Google GKE / Oracle OKE / DigitalOcean DOKS
- Use Kafka on Confluent/Redpanda Cloud (or self-hosted Strimzi)
- CI/CD pipeline with GitHub Actions
- Monitoring and logging setup

**Success Criteria**:
- ✅ All Advanced Level features implemented
- ✅ Kafka event-driven architecture working
- ✅ Dapr integration complete (Pub/Sub, State, Jobs API, Secrets)
- ✅ Deployed on cloud K8s (AKS/GKE/OKE/DOKS)
- ✅ CI/CD pipeline operational

### Bonus Points (Optional)

| Feature | Points | Description |
|---------|--------|-------------|
| Reusable Intelligence | +200 | Create and use Claude Code Subagents and Agent Skills |
| Cloud-Native Blueprints | +200 | Create and use blueprints via Agent Skills for deployment |
| Multi-language Support | +100 | Support Urdu in chatbot |
| Voice Commands | +200 | Add voice input for todo commands |

**Maximum Bonus**: 600 points
**Maximum Total Score**: 1,600 points (1,000 base + 600 bonus)

## Constraints

### Hard Constraints (Cannot Be Changed)

✅ Spec-Driven Development is mandatory. No manual coding allowed.
✅ Windows users MUST use WSL 2. No native Windows development.
✅ Phase order MUST be followed. No skipping phases.
✅ Tech stack is immutable. Cannot swap Next.js, FastAPI, SQLModel, Neon, etc.
✅ MCP Server MUST use Official MCP SDK. No custom implementations.
✅ Stateless architecture required. No in-memory sessions.

### Soft Constraints (Can Add, Not Replace)

✅ Can add additional libraries (e.g., lodash, d3, chart.js) if needed.
✅ Can add monitoring tools (Prometheus, Grafana) in Phase V.
✅ Can add testing frameworks (pytest, jest) for quality assurance.

### Copyright Compliance (Critical)

- 15+ words from any single source is a SEVERE VIOLATION.
- ONE quote per source MAXIMUM.
- DEFAULT to paraphrasing; quotes should be rare exceptions.
- Never reproduce song lyrics, poems, or haikus.
- All submitted documentation MUST pass plagiarism checks.

## Success Criteria

### Evaluation Criteria

**Code Quality (30%)**

- Spec traceability: Every feature maps to a spec
- Clean architecture: Separation of concerns maintained
- Type safety: Python type hints, TypeScript strict mode
- Error handling: Graceful failures, user-friendly messages

**Functional Completeness (40%)**

- All required features implemented per phase
- Natural language commands work as specified (Phase III+)
- Multi-user isolation enforced (Phase II+)
- Event-driven architecture functional (Phase V)

**Spec-Driven Rigor (20%)**

- Spec history documented in /specs folder
- CLAUDE.md instructions clear and actionable
- Spec-Kit workflow followed (Specify → Plan → Tasks → Implement)
- Iterative refinement visible in spec history

**Innovation & Bonus Features (10%)**

- Reusable Intelligence (Subagents, Agent Skills)
- Cloud-Native Blueprints
- Multi-language support (Urdu)
- Voice commands

### Submission Requirements (All Phases)

✅ Public GitHub repository with clear folder structure
✅ `/specs` folder with all specification files
✅ CLAUDE.md and AGENTS.md present
✅ README.md with comprehensive setup instructions
✅ Deployed application URL (Vercel for frontend, cloud for backend)
✅ Demo video (≤ 90 seconds, judges watch only first 90 seconds)
✅ WhatsApp number for live presentation invitation

### Failure Modes to Avoid

❌ Manual coding instead of spec-driven development → Auto-disqualification
❌ Skipping phases → Submission rejected
❌ Using localStorage/sessionStorage in artifacts → Artifacts fail in Claude.ai
❌ Hardcoding credentials → Security violation, points deducted
❌ Stateful servers (in-memory sessions) → Fails horizontal scaling requirement
❌ Not using MCP for Phase III → Misses core architectural learning
❌ Plagiarism in documentation → Severe penalty (see copyright rules)

## Governance

### Amendment Process

1. **Proposal**: Any change to this constitution MUST be proposed with clear rationale.
2. **Documentation**: All amendments MUST be documented with version bump and impact analysis.
3. **Migration Plan**: Breaking changes require migration strategy for existing work.
4. **Approval**: Constitution changes require explicit user consent.

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions.
- **MINOR**: New principle/section added or materially expanded guidance.
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements.

### Compliance Review

- All PRs/reviews MUST verify compliance with constitution principles.
- Complexity MUST be justified when violating simplicity principles.
- Use CLAUDE.md for runtime development guidance aligned with constitution.

### Source of Truth Hierarchy

When conflicts arise, this order applies:

1. **This Constitution** - Immutable principles
2. **Hackathon Brief** (original document) - Official requirements
3. **Specify Files** - Feature requirements
4. **Plan Files** - Implementation approach
5. **Task Files** - Atomic work units

### Key Dates (Non-Negotiable)

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Hackathon Start | Monday, Dec 2, 2025 | Documentation released |
| Phase I Due | Sunday, Dec 8, 2025 | Console app checkpoint |
| Phase II Due | Sunday, Dec 15, 2025 | Web app checkpoint |
| Phase III Due | Sunday, Dec 22, 2025 | Chatbot checkpoint |
| Phase IV Due | Sunday, Jan 5, 2026 | Local K8s checkpoint |
| Phase V Due | Sunday, Jan 19, 2026 | Cloud deployment complete |
| Live Presentations | Sundays (Dec 8, 15, 22; Jan 5, 19) | Top submissions present |

**Submission Form**: https://forms.gle/KMKEKaFUD6ZX4UtY8
**Zoom Link**: https://us06web.zoom.us/j/84976847088?pwd=...
**Meeting Time**: 8:00 PM PKT

---

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31

---

## Acknowledgments

This hackathon is organized by Panaversity, PIAIC, and GIAIC to cultivate the next generation of AI-native software architects.

Top performers may be invited to:
- Join the Panaversity core team
- Step into a startup founder role within the ecosystem
- Teach at Panaversity, PIAIC, and GIAIC

**Founders**: Zia Khan, Rehan, Junaid, Wania

---

_"The future of software development is AI-native and spec-driven. As AI agents like Claude Code become more powerful, the role of the engineer shifts from 'syntax writer' to 'system architect.'"_
